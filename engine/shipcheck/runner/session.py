"""SessionRunner — 한 페르소나 × 한 제품의 전체 세션 루프.

파이프라인:
  [A] AsyncBrowserEnv.observe()
  [B] Cognitive Load (deterministic)
  [C] OCC → PAD + SDE noise + decay (deterministic)
  [D] Chain-of-Emotion LLM 콜 (감정 확정)
  [E] 이탈 판정 (deterministic)
  [F] Action Decision LLM 콜 (행동 결정)
  [G] AsyncBrowserEnv.step(action)
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

import numpy as np

from ..core.types import (
    Action, ActionType, EmotionState, Observation, PADVector, StepLog, SessionLog,
)
from ..layer1_persona.models import PersonaProfile
from ..layer3_emotion.engine import (
    classify_event, compute_pad_delta, update_pad,
    compute_cognitive_load, check_abandonment, OCC_LABEL_MAPPING,
)
from ..llm.claude_cli import ClaudeCli
from ..data.collector import DataCollector
from ..review.generator import generate_review, SyntheticReview, save_reviews

logger = logging.getLogger(__name__)


class SessionRunner:
    """한 페르소나 × 한 제품의 완전한 세션."""

    def __init__(
        self,
        profile: PersonaProfile,
        browser_env,  # BrowserEnv (context manager 밖에서 받음)
        product_url: str,
        product_name: str,
        collector: DataCollector,
        llm: ClaudeCli,
        prompts: dict[str, str],  # {"emotion_eval": template, "action_decide": template}
        max_steps: int = 25,
        rng_seed: int | None = None,
    ) -> None:
        self.profile = profile
        self.env = browser_env
        self.product_url = product_url
        self.product_name = product_name
        self.collector = collector
        self.llm = llm
        self.prompts = prompts
        self.max_steps = max_steps
        self.rng = np.random.default_rng(rng_seed)

        # 세션 상태
        self.session_id = f"{profile.persona_id}_{product_name}_{uuid.uuid4().hex[:6]}"
        # 자발적으로 제품을 열어본 사람 → 살짝 긍정적 초기 상태
        self.pad = PADVector(pleasure=0.1, arousal=0.1, dominance=0.1)
        self.emotion_state = EmotionState()
        self.consecutive_failures = 0
        self.step_count = 0
        self.pages_visited: list[str] = []
        self.recent_actions: list[dict[str, Any]] = []
        self.back_nav_count = 0
        self.hesitation_count = 0
        self.prev_action_succeeded = True
        self.prev_url = ""
        self.session_history: list[str] = []  # 스텝별 1줄 요약 누적

    async def run(self) -> SessionLog:
        """세션 실행. SessionLog 반환."""
        logger.info("세션 시작: %s → %s", self.profile.name, self.product_name)
        start_time = time.time()
        terminated_by = "max_steps"
        abandonment_step = None

        # 초기 페이지 이동
        obs = await self.env.navigate(self.product_url)
        self.pages_visited.append(obs.url)
        self.prev_url = obs.url

        for step_idx in range(self.max_steps):
            self.step_count = step_idx

            # === [B] Cognitive Load (deterministic) ===
            cog_load = compute_cognitive_load(
                obs.element_count, obs.text_length, self.profile.digital_literacy
            )

            # === [C] OCC → PAD + SDE noise + decay ===
            url_changed = obs.url != self.prev_url
            occ_event = classify_event(
                prev_action_succeeded=self.prev_action_succeeded,
                url_changed=url_changed,
                error_in_dom=self._check_error_in_dom(obs.html_summary),
                page_element_count=obs.element_count,
                consecutive_failures=self.consecutive_failures,
                is_first_step=(step_idx == 0),
            )
            pad_delta = compute_pad_delta(
                occ_event, self.profile.params.emotional_volatility,
                self.consecutive_failures, self.rng,
            )
            self.pad = update_pad(self.pad, pad_delta, self.profile.params.emotion_decay_rate)
            emotion_label = OCC_LABEL_MAPPING[occ_event]

            # === [D] 페르소나 반응: 스크린샷 보고 감정 + 의도 ===
            screenshot_path = await self.env.take_screenshot(f"{self.session_id}_step{step_idx}")
            logger.info(
                "  [%s] [step %d] 🧠 페르소나 반응 중... (OCC=%s, PAD=%.2f/%.2f/%.2f, load=%.2f)",
                self.profile.name, step_idx, occ_event.value,
                self.pad.pleasure, self.pad.arousal, self.pad.dominance, cog_load,
            )
            persona_result = self._call_persona_react(obs, cog_load, emotion_label, screenshot_path)
            self.emotion_state = EmotionState(
                pad=self.pad,
                labels=[persona_result.get("intent_type", emotion_label)],
                chain_reasoning=persona_result.get("emotion_reasoning", ""),
                abandonment_risk=persona_result.get("abandonment_risk", 0.0),
            )
            pu = persona_result.get("perceived_usefulness", 0.5)
            peou = persona_result.get("perceived_ease_of_use", 0.5)
            confidence = persona_result.get("confidence", 0.5)
            hesitation = persona_result.get("hesitation", False)
            intent = persona_result.get("intent", "")
            intent_type = persona_result.get("intent_type", "scroll_down")

            # 세션 히스토리
            emotion_reasoning_full = persona_result.get("emotion_reasoning", "")
            last_action_desc = (
                f"{self.recent_actions[-1]['action']} {self.recent_actions[-1].get('target', '')}"
                if self.recent_actions else "첫 페이지 로드"
            )
            self.session_history.append(
                f"step {step_idx}: {obs.url.split('/')[-1] or obs.url} | "
                f"{last_action_desc} → {emotion_label} (P={self.pad.pleasure:.2f}) | "
                f"{emotion_reasoning_full}"
            )

            logger.info(
                "  [%s] [step %d] 💭 PU=%.1f PEOU=%.1f | %s",
                self.profile.name, step_idx, pu, peou, emotion_reasoning_full,
            )
            logger.info(
                "  [%s] [step %d] 💬 의도: [%s] %s (conf=%.1f%s)",
                self.profile.name, step_idx,
                intent_type, intent, confidence,
                " 🤔" if hesitation else "",
            )

            if hesitation:
                self.hesitation_count += 1

            # === [E] 이탈 판정 (deterministic + 페르소나 give_up) ===
            if intent_type == "give_up":
                step_log = self._make_step_log(
                    step_idx, obs, cog_load, pu, peou,
                    Action(ActionType.TERMINATE, reasoning=intent),
                    confidence=confidence, hesitation=hesitation, elements_considered=0,
                    should_abandon=True, abandon_reason=f"페르소나 자발적 이탈: {intent}",
                )
                self.collector.record_step(step_log)
                terminated_by = "abandoned"
                abandonment_step = step_idx
                logger.info("  [%s] [step %d] 🚪 자발적 이탈: %s", self.profile.name, step_idx, intent)
                break

            should_abandon, abandon_reason = check_abandonment(
                self.pad, self.consecutive_failures,
                self.profile.params.error_tolerance,
                self.profile.params.pleasure_abandon_threshold,
                cog_load, step_idx,
            )
            if should_abandon:
                step_log = self._make_step_log(
                    step_idx, obs, cog_load, pu, peou,
                    Action(ActionType.TERMINATE, reasoning=abandon_reason or "이탈"),
                    confidence=0.0, hesitation=False, elements_considered=0,
                    should_abandon=True, abandon_reason=abandon_reason,
                )
                self.collector.record_step(step_log)
                terminated_by = "abandoned"
                abandonment_step = step_idx
                logger.info("  [%s] [step %d] 🚪 시스템 이탈: %s", self.profile.name, step_idx, abandon_reason)
                break

            # === [F] 액션 실행기: 의도 → 정확한 브라우저 액션 ===
            logger.info("  [%s] [step %d] 🎯 액션 실행기...", self.profile.name, step_idx)
            action_result = self._call_action_executor(obs, persona_result, screenshot_path)
            action = self._parse_action(action_result)

            logger.info(
                "  [%s] [step %d] ▶ %s %s — %s",
                self.profile.name, step_idx,
                action.action_type.value,
                action.target or "",
                action_result.get("reasoning", ""),
            )

            # 스텝 로그 기록
            step_log = self._make_step_log(
                step_idx, obs, cog_load, pu, peou, action,
                confidence, hesitation, elements_considered=obs.element_count,
            )
            self.collector.record_step(step_log)

            # Terminate 체크 (액션 실행기가 terminate를 반환한 경우)
            if action.action_type == ActionType.TERMINATE:
                terminated_by = "abandoned"
                abandonment_step = step_idx
                logger.info("  [%s] [step %d] 🚪 실행기 terminate", self.profile.name, step_idx)
                break

            # === [G] 브라우저 액션 실행 ===
            if action.action_type == ActionType.BACK:
                self.back_nav_count += 1

            self.prev_url = obs.url
            obs, succeeded = await self._execute_browser_action(action)
            self.prev_action_succeeded = succeeded
            logger.info(
                "  [%s] [step %d] %s → %s",
                self.profile.name, step_idx,
                "✅" if succeeded else "❌",
                obs.url if obs.url != self.prev_url else "(같은 페이지)",
            )

            if succeeded:
                self.consecutive_failures = 0
            else:
                self.consecutive_failures += 1

            if obs.url not in self.pages_visited:
                self.pages_visited.append(obs.url)

            # 최근 행동 이력 유지 (최대 5개)
            self.recent_actions.append({
                "step": step_idx,
                "action": action.action_type.value,
                "target": action.target,
                "outcome": "success" if succeeded else "failure",
            })
            if len(self.recent_actions) > 5:
                self.recent_actions.pop(0)

        # 세션 로그
        elapsed = time.time() - start_time
        session_log = SessionLog(
            session_id=self.session_id,
            persona_id=self.profile.persona_id,
            segment=self.profile.segment,
            product_name=self.product_name,
            product_url=self.product_url,
            total_steps=self.step_count + 1,
            terminated_by=terminated_by,
            abandonment_step=abandonment_step,
            final_pad_pleasure=self.pad.pleasure,
            final_pad_arousal=self.pad.arousal,
            final_pad_dominance=self.pad.dominance,
            final_perceived_usefulness=pu,
            final_perceived_ease_of_use=peou,
            pages_visited=self.pages_visited,
            unique_pages=len(set(self.pages_visited)),
            total_back_navigations=self.back_nav_count,
            total_hesitations=self.hesitation_count,
            openness=self.profile.big_five.openness,
            conscientiousness=self.profile.big_five.conscientiousness,
            extraversion=self.profile.big_five.extraversion,
            agreeableness=self.profile.big_five.agreeableness,
            neuroticism=self.profile.big_five.neuroticism,
            digital_literacy=self.profile.digital_literacy,
        )
        self.collector.record_session(session_log)
        logger.info(
            "세션 완료: %s → %s, steps=%d, terminated=%s, pleasure=%.2f",
            self.profile.name, self.product_name,
            self.step_count + 1, terminated_by, self.pad.pleasure,
        )

        # 리뷰 생성 — 세션 로그 저장 후, 반환 전
        self._generate_review(session_log)

        return session_log

    # ------------------------------------------------------------------
    # LLM 호출
    # ------------------------------------------------------------------

    DIGITAL_LITERACY_DESC = {
        1: "컴퓨터를 거의 사용하지 않음. 아이콘에 의존하고 텍스트 메뉴를 회피.",
        2: "기본적인 앱은 사용하지만 새로운 도구에는 불안감을 느낌.",
        3: "일반적인 웹 앱을 무리 없이 사용. 가끔 혼란을 겪음.",
        4: "다양한 SaaS를 자유롭게 사용. 키보드 단축키, 빠른 탐색에 익숙.",
    }

    BEHAVIOR_STYLE = {
        1: (
            "당신은 화면을 읽는 데 오래 걸리고, 버튼을 누르기 전에 한참 망설입니다. "
            "모르는 것은 절대 누르지 않고, 익숙한 패턴(큰 버튼, 아이콘)만 따릅니다. "
            "실수하면 패닉하고, 되돌리는 방법을 모릅니다."
        ),
        2: (
            "당신은 기본적인 클릭과 입력은 하지만, 새로운 UI에서는 신중합니다. "
            "익숙한 도구(Google Forms 등)와 비교하면서 '이건 왜 이러지'라고 자주 생각합니다. "
            "잘못 누를까봐 조심하고, 확실한 것만 시도합니다."
        ),
        3: (
            "당신은 대부분의 웹 앱을 무리 없이 사용합니다. "
            "새 기능이 보이면 눌러보고, 실패하면 다른 방법을 시도합니다. "
            "읽기보다 직접 해보면서 파악하는 편입니다."
        ),
        4: (
            "당신은 새 도구를 빠르게 평가하는 데 익숙한 파워유저입니다. "
            "스크롤하며 구경하기보다 직접 입력하고, 단축키(/, @, Ctrl+K 등)를 시도하고, "
            "설정 패널을 열어보고, 기능 한계를 테스트합니다. "
            "관찰보다 조작이 우선이고, '이게 되나?'를 직접 해봐서 확인합니다. "
            "5번 이상 연속 스크롤만 하고 있다면 뭔가 잘못하고 있는 것입니다 — 직접 무언가를 만들어보십시오."
        ),
    }

    def _call_persona_react(
        self, obs: Observation, cog_load: float, emotion_label: str,
        screenshot_path: Path | None,
    ) -> dict[str, Any]:
        """페르소나 반응: 스크린샷을 보고 감정 + 의도 출력."""
        params = self.profile.params
        sycophancy_instruction = ""
        if params.sycophancy_resistance > 0.5:
            sycophancy_instruction = (
                f"당신의 비판 성향은 {params.sycophancy_resistance:.2f}입니다. "
                "제품에 관대하지 마십시오. 불편한 점은 직접적으로 표현하십시오."
            )

        history_str = "\n".join(self.session_history[-15:]) or "없음 (첫 스텝)"

        prompt = self.prompts["persona_react"].format(
            persona_name=self.profile.name,
            background_narrative=self.profile.background_narrative,
            age=self.profile.demographics.get("age", ""),
            occupation=self.profile.demographics.get("occupation", ""),
            digital_literacy_desc=self.DIGITAL_LITERACY_DESC.get(self.profile.digital_literacy, ""),
            error_tolerance=params.error_tolerance,
            emotional_volatility=f"{params.emotional_volatility:.2f}",
            exploration_tendency=f"{params.exploration_tendency:.2f}",
            sycophancy_resistance=f"{params.sycophancy_resistance:.2f}",
            satisficing_threshold=f"{params.satisficing_threshold:.2f}",
            digital_literacy=self.profile.digital_literacy,
            jtbd_goal=self.profile.jtbd.primary_goal,
            success_criterion=self.profile.jtbd.success_criterion,
            prior_tools=", ".join(self.profile.jtbd.prior_tools) or "없음",
            session_history=history_str,
            pad_pleasure=f"{self.pad.pleasure:.2f}",
            pad_arousal=f"{self.pad.arousal:.2f}",
            pad_dominance=f"{self.pad.dominance:.2f}",
            emotion_label=emotion_label,
            sycophancy_instruction=sycophancy_instruction,
            behavior_style_instruction=self.BEHAVIOR_STYLE.get(self.profile.digital_literacy, ""),
        )

        try:
            if screenshot_path and screenshot_path.exists():
                return self.llm.complete_json_with_image(
                    prompt, image_path=screenshot_path,
                )
            else:
                # 스크린샷 없으면 텍스트 전용 fallback
                return self.llm.complete_json(prompt)
        except Exception as e:
            logger.warning("persona_react LLM 실패: %s — fallback", e)
            return {
                "emotion_reasoning": f"[LLM 실패] 현재 {emotion_label} 상태",
                "intent": "아래로 스크롤해서 더 보고 싶다",
                "intent_type": "scroll_down",
                "type_value": None,
                "confidence": 0.3,
                "hesitation": True,
                "perceived_usefulness": 0.5,
                "perceived_ease_of_use": 0.5,
                "abandonment_risk": 0.3,
            }

    def _call_action_executor(
        self, obs: Observation, persona_result: dict[str, Any],
        screenshot_path: Path | None,
    ) -> dict[str, Any]:
        """액션 실행기: 페르소나 의도 + 접근성 트리 + 스크린샷 → 정확한 액션."""
        intent = persona_result.get("intent", "")
        intent_type = persona_result.get("intent_type", "click_element")
        type_value = persona_result.get("type_value")

        # 접근성 스냅샷 (YAML) — parser.js 대신 Playwright 네이티브
        # html_summary에 이미 접근성 스냅샷 YAML이 들어있음
        snapshot = obs.html_summary
        if len(snapshot) > 6000:
            snapshot = snapshot[:6000] + "\n... (truncated)"

        prompt = self.prompts["action_executor"].format(
            intent=intent,
            intent_type=intent_type,
            type_value=type_value or "null",
            current_url=obs.url,
            scroll_pct=int(obs.scroll_ratio * 100),
            accessibility_snapshot=snapshot,
        )

        try:
            if screenshot_path and screenshot_path.exists():
                return self.llm.complete_json_with_image(
                    prompt, image_path=screenshot_path,
                )
            else:
                return self.llm.complete_json(prompt)
        except Exception as e:
            logger.warning("action_executor LLM 실패: %s — scroll fallback", e)
            return {
                "action": "scroll",
                "target": None,
                "value": "down",
                "reasoning": "[LLM 실패] 스크롤",
            }

    # ------------------------------------------------------------------
    # 리뷰 생성
    # ------------------------------------------------------------------

    def _generate_review(self, session_log: SessionLog) -> None:
        """세션 종료 후 G2 스타일 리뷰를 생성하고 저장.

        session_history에 누적된 emotion_reasoning을 기반으로
        review/generator.py의 파이프라인을 호출한다.
        """
        try:
            # collector에 기록된 step 로그를 복원
            step_logs = self._load_step_logs()

            review = generate_review(
                persona=self.profile,
                session_log=session_log,
                step_logs=step_logs,
                llm_complete_json=self.llm.complete_json,
            )

            # runs/{experiment_id}/reviews/{persona}_{product}.json 에 저장
            reviews_dir = self.collector.output_dir / "reviews"
            reviews_dir.mkdir(parents=True, exist_ok=True)

            # 파일명: 페르소나ID_제품명.json (안전한 파일명)
            safe_persona = self.profile.persona_id.replace("/", "_").replace(" ", "_")
            safe_product = self.product_name.replace("/", "_").replace(" ", "_")
            review_path = reviews_dir / f"{safe_persona}_{safe_product}.json"

            review_data = {
                "persona_id": review.persona_id,
                "persona_name": review.persona_name,
                "role_id": review.role_id,
                "segment": review.segment,
                "product_name": review.product_name,
                "likes": review.likes,
                "dislikes": review.dislikes,
                "problems_solved": review.problems_solved,
                "overall_rating": review.overall_rating,
                "review_reasoning": review.review_reasoning,
                "experience_summary_hash": review.experience_summary_hash,
                "generation_method": review.generation_method,
            }
            review_path.write_text(
                json.dumps(review_data, ensure_ascii=False, indent=2)
            )
            logger.info(
                "리뷰 생성 완료: %s → %s (rating=%.1f) → %s",
                self.profile.name, self.product_name,
                review.overall_rating, review_path,
            )
        except Exception as e:
            logger.warning("리뷰 생성 실패 (%s → %s): %s", self.profile.name, self.product_name, e)

    def _load_step_logs(self) -> list[StepLog]:
        """collector의 JSONL에서 이 세션의 step 로그를 로드."""
        steps_path = self.collector.output_dir / "steps.jsonl"
        step_logs: list[StepLog] = []
        if not steps_path.exists():
            return step_logs

        with open(steps_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                # 이 세션의 step만 필터 — session_id 필드가 없으므로
                # experiment_id + 순서 기반으로 최근 N개 step을 사용
                step_logs.append(StepLog(
                    step_index=data["step_index"],
                    url=data["url"],
                    action_type=data["action_type"],
                    action_target=data.get("action_target"),
                    action_reasoning=data.get("action_reasoning", ""),
                    pad_pleasure=data["pad_pleasure"],
                    pad_arousal=data["pad_arousal"],
                    pad_dominance=data["pad_dominance"],
                    emotion_labels=data.get("emotion_labels", []),
                    emotion_reasoning=data.get("emotion_reasoning", ""),
                    abandonment_risk=data.get("abandonment_risk", 0.0),
                    cognitive_load=data.get("cognitive_load", 0.0),
                    perceived_usefulness=data.get("perceived_usefulness", 0.5),
                    perceived_ease_of_use=data.get("perceived_ease_of_use", 0.5),
                    confidence=data.get("confidence", 0.5),
                    hesitation=data.get("hesitation", False),
                    elements_considered=data.get("elements_considered", 0),
                    should_abandon=data.get("should_abandon", False),
                    abandon_reason=data.get("abandon_reason"),
                ))

        # JSONL에는 모든 세션의 step이 섞여 있으므로,
        # 이 세션의 step 수만큼 마지막에서 가져옴
        total_steps = self.step_count + 1
        if len(step_logs) >= total_steps:
            step_logs = step_logs[-total_steps:]
        return step_logs

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _parse_action(self, result: dict[str, Any]) -> Action:
        """LLM 출력 → Action dataclass.

        playwright-cli 모드: ref(e15), target(인덱스) 모두 지원.
        """
        action_str = result.get("action", "scroll")
        try:
            action_type = ActionType(action_str)
        except ValueError:
            action_type = ActionType.SCROLL

        # ref 또는 target
        target = result.get("ref") or result.get("target")
        if target is not None:
            target = str(target)

        return Action(
            action_type=action_type,
            target=target,
            value=result.get("value"),
            reasoning=result.get("reasoning", ""),
        )

    async def _execute_browser_action(self, action: Action) -> tuple[Observation, bool]:
        """Action → PlaywrightCliEnv 명령 실행.

        PlaywrightCliEnv의 ref 기반 메서드 또는 기존 step() 호출.
        """
        from ..browser.pw_cli_env import PlaywrightCliEnv

        # PlaywrightCliEnv인 경우 직접 명령 매핑
        if isinstance(self.env, PlaywrightCliEnv):
            try:
                if action.action_type == ActionType.CLICK:
                    if not action.target:
                        return await self.env.scroll(), False
                    return await self.env.click(action.target)

                elif action.action_type == ActionType.TYPE:
                    if action.value:
                        return await self.env.type_text(action.value)
                    return await self.env.scroll(), False

                elif action.action_type == ActionType.FILL:
                    if action.target and action.value:
                        return await self.env.fill(action.target, action.value)
                    return await self.env.scroll(), False

                elif action.action_type in (ActionType.KEY_PRESS, ActionType.PRESS):
                    if action.value:
                        return await self.env.press(action.value)
                    return await self.env.scroll(), False

                elif action.action_type == ActionType.SCROLL:
                    direction = (action.value or "down").lower()
                    return await self.env.scroll(direction)

                elif action.action_type == ActionType.BACK:
                    return await self.env.go_back()

                elif action.action_type == ActionType.HOVER:
                    if action.target:
                        return await self.env.hover(action.target)
                    return await self.env.scroll(), False

                elif action.action_type == ActionType.SELECT:
                    if action.target and action.value:
                        return await self.env.select(action.target, action.value)
                    return await self.env.scroll(), False

                elif action.action_type == ActionType.TERMINATE:
                    obs = await self.env._observe()
                    return obs, True

                else:
                    return await self.env.scroll(), False

            except Exception as e:
                logger.warning("브라우저 액션 실패: %s — %s", action, e)
                obs = await self.env._observe()
                return obs, False

        # 기존 AsyncBrowserEnv인 경우
        return await self.env.step(action)

    def _make_step_log(
        self, step_idx, obs, cog_load, pu, peou, action,
        confidence, hesitation, elements_considered,
        should_abandon=False, abandon_reason=None,
    ) -> StepLog:
        return StepLog(
            step_index=step_idx,
            url=obs.url,
            action_type=action.action_type.value,
            action_target=action.target,
            action_reasoning=action.reasoning,
            pad_pleasure=self.pad.pleasure,
            pad_arousal=self.pad.arousal,
            pad_dominance=self.pad.dominance,
            emotion_labels=list(self.emotion_state.labels),
            emotion_reasoning=self.emotion_state.chain_reasoning,
            abandonment_risk=self.emotion_state.abandonment_risk,
            cognitive_load=cog_load,
            perceived_usefulness=pu,
            perceived_ease_of_use=peou,
            confidence=confidence,
            hesitation=hesitation,
            elements_considered=elements_considered,
            should_abandon=should_abandon,
            abandon_reason=abandon_reason,
        )

    @staticmethod
    def _check_error_in_dom(dom_text: str) -> bool:
        """직렬화된 DOM 텍스트에서 에러 메시지 패턴 탐지."""
        import re
        text_lower = dom_text.lower()
        error_patterns = [
            r"\b404\b", r"\b500\b", r"\berror\b", r"\bfailed\b",
            r"not found", r"오류", r"실패", r"문제가 발생",
        ]
        return any(re.search(p, text_lower) for p in error_patterns)
