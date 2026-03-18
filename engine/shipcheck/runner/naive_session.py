"""NaiveSessionRunner — Ablation 조건: 파이프라인 없이 단일 LLM 콜만.

비교 대상:
  - Full pipeline: OCC → SDE → PAD → Chain-of-Emotion LLM → 이탈판정 → Action LLM
  - Naive (이 파일): 페르소나 서술 + 단일 LLM 콜 → action + emotion 동시 출력

차이점:
  - OCC/SDE/PAD 계산 없음 — 감정은 LLM이 자유롭게 결정
  - 이탈 판정 없음 — LLM이 terminate를 선택해야만 이탈
  - 스텝당 LLM 콜 1회 (full은 2회)
"""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path
from typing import Any

from ..core.types import (
    Action, ActionType, EmotionState, Observation, PADVector, StepLog, SessionLog,
)
from ..layer1_persona.models import PersonaProfile
from ..llm.claude_cli import ClaudeCli
from ..data.collector import DataCollector

logger = logging.getLogger(__name__)

DIGITAL_LITERACY_DESC = {
    1: "컴퓨터를 거의 사용하지 않음. 아이콘에 의존하고 텍스트 메뉴를 회피.",
    2: "기본적인 앱은 사용하지만 새로운 도구에는 불안감을 느낌.",
    3: "일반적인 웹 앱을 무리 없이 사용. 가끔 혼란을 겪음.",
    4: "다양한 SaaS를 자유롭게 사용. 키보드 단축키, 빠른 탐색에 익숙.",
}


class NaiveSessionRunner:
    """Ablation 조건: 파이프라인 없는 단일 LLM 콜 세션."""

    def __init__(
        self,
        profile: PersonaProfile,
        browser_env,
        product_url: str,
        product_name: str,
        collector: DataCollector,
        llm: ClaudeCli,
        prompt_template: str,
        max_steps: int = 25,
    ) -> None:
        self.profile = profile
        self.env = browser_env
        self.product_url = product_url
        self.product_name = product_name
        self.collector = collector
        self.llm = llm
        self.prompt_template = prompt_template
        self.max_steps = max_steps

        self.session_id = f"{profile.persona_id}_{product_name}_naive_{uuid.uuid4().hex[:6]}"
        self.step_count = 0
        self.pages_visited: list[str] = []
        self.recent_actions: list[dict[str, Any]] = []
        self.session_history: list[str] = []
        self.back_nav_count = 0
        self.hesitation_count = 0
        self.last_pu = 0.5
        self.last_peou = 0.5

    def run(self) -> SessionLog:
        logger.info("세션 시작 [NAIVE]: %s → %s", self.profile.name, self.product_name)
        start_time = time.time()
        terminated_by = "max_steps"
        abandonment_step = None

        obs = self.env.navigate(self.product_url)
        self.pages_visited.append(obs.url)

        for step_idx in range(self.max_steps):
            self.step_count = step_idx

            # === 단일 LLM 콜: 감정 + 행동 동시 결정 ===
            logger.info(
                "  [%s][NAIVE] [step %d] 🎯 단일 콜 중... (%s)",
                self.profile.name, step_idx, obs.url.split("/")[-1] or obs.url,
            )
            result = self._call_naive(obs)

            emotion_reasoning = result.get("emotion_reasoning", "")
            action = self._parse_action(result)
            confidence = result.get("confidence", 0.5)
            hesitation = result.get("hesitation", False)
            elements_considered = result.get("elements_considered", 1)
            pu = result.get("perceived_usefulness", 0.5)
            peou = result.get("perceived_ease_of_use", 0.5)
            abandonment_risk = result.get("abandonment_risk", 0.0)
            self.last_pu = pu
            self.last_peou = peou

            if hesitation:
                self.hesitation_count += 1

            # 세션 히스토리
            last_action_desc = (
                f"{self.recent_actions[-1]['action']} {self.recent_actions[-1].get('target', '')}"
                if self.recent_actions else "첫 페이지 로드"
            )
            self.session_history.append(
                f"step {step_idx}: {obs.url.split('/')[-1] or obs.url} | "
                f"{last_action_desc} | {emotion_reasoning}"
            )

            logger.info(
                "  [%s][NAIVE] [step %d] 💭 PU=%.1f PEOU=%.1f risk=%.1f | %s",
                self.profile.name, step_idx, pu, peou, abandonment_risk,
                emotion_reasoning,
            )
            logger.info(
                "  [%s][NAIVE] [step %d] ▶ %s %s (conf=%.1f%s) — %s",
                self.profile.name, step_idx,
                action.action_type.value,
                action.target or "",
                confidence,
                " 🤔" if hesitation else "",
                action.reasoning,
            )

            # 스텝 로그 (PAD는 0으로 — naive에는 PAD 계산 없음)
            step_log = StepLog(
                step_index=step_idx,
                url=obs.url,
                action_type=action.action_type.value,
                action_target=action.target,
                action_reasoning=action.reasoning,
                pad_pleasure=0.0,  # naive: PAD 없음
                pad_arousal=0.0,
                pad_dominance=0.0,
                emotion_labels=[],
                emotion_reasoning=emotion_reasoning,
                abandonment_risk=abandonment_risk,
                cognitive_load=0.0,  # naive: cognitive load 없음
                perceived_usefulness=pu,
                perceived_ease_of_use=peou,
                confidence=confidence,
                hesitation=hesitation,
                elements_considered=elements_considered,
                should_abandon=(action.action_type == ActionType.TERMINATE),
                abandon_reason="LLM decided to terminate" if action.action_type == ActionType.TERMINATE else None,
            )
            self.collector.record_step(step_log)

            if action.action_type == ActionType.TERMINATE:
                terminated_by = "abandoned"
                abandonment_step = step_idx
                logger.info("  [%s][NAIVE] 이탈: step=%d", self.profile.name, step_idx)
                break

            if action.action_type == ActionType.BACK:
                self.back_nav_count += 1

            prev_url = obs.url
            obs, succeeded = self.env.step(action)

            logger.info(
                "  [%s][NAIVE] [step %d] %s → %s",
                self.profile.name, step_idx,
                "✅" if succeeded else "❌",
                obs.url if obs.url != prev_url else "(같은 페이지)",
            )

            if obs.url not in self.pages_visited:
                self.pages_visited.append(obs.url)

            self.recent_actions.append({
                "step": step_idx,
                "action": action.action_type.value,
                "target": action.target,
                "outcome": "success" if succeeded else "failure",
            })
            if len(self.recent_actions) > 5:
                self.recent_actions.pop(0)

            self.env.take_screenshot(f"{self.session_id}_step{step_idx}")

        elapsed = time.time() - start_time
        session_log = SessionLog(
            session_id=self.session_id,
            persona_id=self.profile.persona_id,
            segment=self.profile.segment + "_naive",  # ablation 구분자
            product_name=self.product_name,
            product_url=self.product_url,
            total_steps=self.step_count + 1,
            terminated_by=terminated_by,
            abandonment_step=abandonment_step,
            final_pad_pleasure=0.0,
            final_pad_arousal=0.0,
            final_pad_dominance=0.0,
            final_perceived_usefulness=self.last_pu,
            final_perceived_ease_of_use=self.last_peou,
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
            "세션 완료 [NAIVE]: %s → %s, steps=%d, terminated=%s",
            self.profile.name, self.product_name,
            self.step_count + 1, terminated_by,
        )
        return session_log

    def _call_naive(self, obs: Observation) -> dict[str, Any]:
        """단일 LLM 콜: 감정 + 행동 동시 결정. 파이프라인 없음."""
        clickable_str = "\n".join(
            f"- {eid}" for eid in (obs.clickable_elements or [])[:30]
        ) or "없음"
        input_str = "\n".join(
            f"- {inp.get('id', '?')} (type={inp.get('type', '?')}, value={inp.get('value', '')})"
            for inp in (obs.input_elements or [])[:15]
        ) or "없음"
        recent_str = "\n".join(
            f"  step {a['step']}: {a['action']} {a.get('target', '')} → {a['outcome']}"
            for a in self.recent_actions
        ) or "없음"
        history_str = "\n".join(self.session_history[-15:]) or "없음 (첫 스텝)"

        html = obs.html_summary
        if len(html) > 8000:
            html = html[:8000] + "\n... (truncated)"

        prompt = self.prompt_template.format(
            persona_name=self.profile.name,
            background_narrative=self.profile.background_narrative,
            age=self.profile.demographics.get("age", ""),
            occupation=self.profile.demographics.get("occupation", ""),
            digital_literacy_desc=DIGITAL_LITERACY_DESC.get(self.profile.digital_literacy, ""),
            jtbd_goal=self.profile.jtbd.primary_goal,
            success_criterion=self.profile.jtbd.success_criterion,
            prior_tools=", ".join(self.profile.jtbd.prior_tools) or "없음",
            session_history=history_str,
            current_url=obs.url,
            scroll_pct=int(obs.scroll_ratio * 100),
            html_summary=html,
            clickable_elements=clickable_str,
            input_elements=input_str,
            recent_actions=recent_str,
        )

        try:
            return self.llm.complete_json(prompt)
        except Exception as e:
            logger.warning("[NAIVE] LLM 실패: %s", e)
            return {
                "emotion_reasoning": "[LLM 실패]",
                "action": "back",
                "target": None,
                "value": None,
                "reasoning": "LLM 실패 — 뒤로가기",
                "confidence": 0.1,
                "hesitation": True,
                "elements_considered": 0,
                "perceived_usefulness": 0.5,
                "perceived_ease_of_use": 0.5,
                "abandonment_risk": 0.5,
            }

    def _parse_action(self, result: dict[str, Any]) -> Action:
        action_str = result.get("action", "back")
        try:
            action_type = ActionType(action_str)
        except ValueError:
            action_type = ActionType.BACK
        return Action(
            action_type=action_type,
            target=result.get("target"),
            value=result.get("value"),
            reasoning=result.get("reasoning", ""),
        )
