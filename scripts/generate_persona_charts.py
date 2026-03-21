#!/usr/bin/env python3
"""사업계획서용 페르소나 시각화 — VC가 3초 만에 이해하는 차트

Chart 1: "같은 제품, 다른 사람" — 3명 비교 카드 + 바 차트
Chart 2: "시스템 역량" — KPI + 매트릭스
"""

import yaml
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
from collections import Counter, defaultdict
import textwrap

# --- 한글 폰트 ---
def setup_korean_font():
    candidates = ["NanumGothic", "NanumBarunGothic", "Noto Sans CJK KR"]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            plt.rcParams["axes.unicode_minus"] = False
            return name
    import subprocess
    r = subprocess.run(["fc-list", ":lang=ko", "--format=%{family}\n"],
                       capture_output=True, text=True)
    if r.stdout.strip():
        first = r.stdout.strip().split("\n")[0].split(",")[0]
        plt.rcParams["font.family"] = first
        plt.rcParams["axes.unicode_minus"] = False
        return first
    return None

def load_personas(d: Path) -> list[dict]:
    return [yaml.safe_load(open(f, encoding="utf-8")) for f in sorted(d.glob("b*.yaml"))]

# --- 상수 ---
BIG_FIVE_KEYS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
BIG_FIVE_KR = ["개방성", "성실성", "외향성", "친화성", "신경성"]

ROLE_KR = {
    "startup_founder": "스타트업 창업자", "small_biz_operator": "소규모 사업자",
    "marketing_pro": "마케팅 전문가", "educator_nonprofit": "교육자 / 비영리",
    "creative_freelancer": "크리에이터 / 프리랜서", "tech_professional": "개발자 / 엔지니어",
}
SEGMENT_KR = {
    "explorer": "탐험형", "power_user": "파워유저", "cautious_methodical": "신중형",
    "intuitive": "직관형", "anxious": "불안형", "calm": "안정형",
    "agreeable": "순응형", "critical_vocal": "비판형", "tech_savvy": "기술친화", "tech_novice": "기술초보",
}

# 색상
C_BG = "#FFFFFF"
C_TITLE = "#1A1A2E"
C_SUB = "#6B7280"
C_ACCENT = "#6C5CE7"
C_RED = "#FF6B6B"
C_TEAL = "#4ECDC4"
C_PURPLE = "#A29BFE"
C_CARD = "#F9FAFB"


# ============================================================
# Chart 1: 3명 비교
# ============================================================
def chart_persona_comparison(personas, out):
    picks = {}
    for p in personas:
        if p["persona_id"] == "b001": picks["A"] = p
        elif p["persona_id"] == "b003": picks["B"] = p
        elif p["persona_id"] == "b020": picks["C"] = p

    trio = [picks["A"], picks["B"], picks["C"]]
    colors = [C_RED, C_PURPLE, C_TEAL]
    labels = ["조심스러운 교육자", "호기심 많은 크리에이터", "까다로운 엔지니어"]
    patterns = [
        ["무료인지 먼저 확인", "조건부 로직 시도 → 실수 걱정에 재확인", "가격 장벽에서 이탈 가능성 ↑"],
        ["디자인/브랜딩부터 탐색", "새 기능 적극 시도", "예쁘면 유료 전환 의향 ↑"],
        ["API/웹훅 스펙 먼저 확인", "문서 품질에 민감", "기술 요건 불충족 → 즉시 이탈"],
    ]

    fig, axes = plt.subplots(1, 3, figsize=(20, 9))
    fig.patch.set_facecolor(C_BG)

    # 헤드라인
    fig.text(0.5, 0.97, "같은 제품을 쓰는 3명의 사용자",
             ha="center", fontsize=28, fontweight="bold", color=C_TITLE)
    fig.text(0.5, 0.935, "성격 · 직업 · 목표가 다르면, 제품 경험도 완전히 달라집니다",
             ha="center", fontsize=14, color=C_SUB)

    for col, (ax, p, color, label, pats) in enumerate(zip(axes, trio, colors, labels, patterns)):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_facecolor(C_BG)

        # 카드 배경
        card = FancyBboxPatch((0.2, 0.2), 9.6, 13.5,
                              boxstyle="round,pad=0.3",
                              facecolor=C_CARD, edgecolor=color, linewidth=3)
        ax.add_patch(card)

        # 상단 컬러 바
        bar = FancyBboxPatch((0.2, 12.5), 9.6, 1.2,
                             boxstyle="round,pad=0.15",
                             facecolor=color, edgecolor="none")
        ax.add_patch(bar)

        # 이름 + 레이블
        ax.text(5, 13.1, p["name"], ha="center", fontsize=22,
                fontweight="bold", color="white")
        ax.text(5, 12.65, label, ha="center", fontsize=12, color="white", alpha=0.9)

        # 프로필 정보
        role_kr = ROLE_KR.get(p["role_id"], p["role_id"])
        seg_kr = SEGMENT_KR.get(p["segment"], p["segment"])
        bs_kr = {"very_high": "매우 높음", "high": "높음",
                 "moderate": "보통", "low": "낮음"}.get(p["budget_sensitivity"], "?")
        dl_kr = {1: "초보", 2: "기본", 3: "중급", 4: "고급"}.get(p["digital_literacy"], "?")
        prior = ", ".join(p["jtbd"].get("prior_tools", []))

        occ = p["demographics"]["occupation"]
        if len(occ) > 35:
            occ = occ[:33] + "…"

        info = [
            ("직업", occ),
            ("유형", f"{role_kr} · {seg_kr}"),
            ("나이 / 숙련도", f"{p['demographics']['age']}세 · 디지털 {dl_kr}"),
            ("가격 민감도", bs_kr),
            ("기존 도구", prior),
        ]

        y = 12.0
        for key, val in info:
            ax.text(0.8, y, key, fontsize=9, color=C_SUB, fontweight="bold")
            ax.text(3.3, y, val, fontsize=9.5, color=C_TITLE)
            y -= 0.55

        # Big Five 수평 바 차트
        y_bar_start = 8.8
        ax.text(5, y_bar_start + 0.4, "Big Five 성격 프로필",
                ha="center", fontsize=11, fontweight="bold", color=C_TITLE)

        for i, (key, kr) in enumerate(zip(BIG_FIVE_KEYS, BIG_FIVE_KR)):
            val = p["big_five"][key]
            y_pos = y_bar_start - i * 0.7

            # 레이블
            ax.text(0.8, y_pos - 0.15, kr, fontsize=9, color=C_SUB, va="center")

            # 배경 바
            bg_bar = FancyBboxPatch((3.0, y_pos - 0.3), 6.2, 0.35,
                                    boxstyle="round,pad=0.05",
                                    facecolor="#E8E8EE", edgecolor="none")
            ax.add_patch(bg_bar)

            # 값 바
            bar_width = val * 6.2
            val_bar = FancyBboxPatch((3.0, y_pos - 0.3), max(bar_width, 0.2), 0.35,
                                     boxstyle="round,pad=0.05",
                                     facecolor=color, edgecolor="none", alpha=0.7)
            ax.add_patch(val_bar)

            # 값 텍스트
            ax.text(3.0 + bar_width + 0.15, y_pos - 0.12,
                    f"{val:.2f}", fontsize=8, color=C_SUB, va="center")

        # 예상 사용 패턴
        y_pat = 4.8
        ax.text(5, y_pat, "예상 사용 패턴", ha="center",
                fontsize=11, fontweight="bold", color=color)

        for i, line in enumerate(pats):
            ax.text(5, y_pat - 0.65 - i * 0.55, f"→ {line}",
                    ha="center", fontsize=10, color=C_TITLE)

        # 목표 (JTBD)
        y_jtbd = 2.4
        ax.text(5, y_jtbd, "이 사람의 목표", ha="center",
                fontsize=10, fontweight="bold", color=C_TITLE)

        jtbd = p["jtbd"]["primary_goal"]
        if len(jtbd) > 80:
            jtbd = jtbd[:78] + "…"
        wrapped = textwrap.fill(jtbd, width=25)
        for i, line in enumerate(wrapped.split("\n")[:3]):
            ax.text(5, y_jtbd - 0.5 - i * 0.45, line,
                    ha="center", fontsize=9, color=C_SUB, style="italic")

    # 하단
    fig.text(0.5, 0.01,
             "ShipCheck은 30명의 다양한 AI 페르소나가 제품을 직접 사용하고 리뷰합니다  ·  6개 직업군 · 10가지 성격유형",
             ha="center", fontsize=11, color=C_SUB, style="italic")

    plt.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.04, wspace=0.08)
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  Saved: {out}")


# ============================================================
# Chart 2: 시스템 역량 총괄
# ============================================================
def chart_system_overview(personas, out):
    roles_order = list(ROLE_KR.keys())
    segs_order = list(SEGMENT_KR.keys())

    counts = defaultdict(int)
    for p in personas:
        counts[(p["role_id"], p["segment"])] += 1
    matrix = np.zeros((len(roles_order), len(segs_order)))
    for i, r in enumerate(roles_order):
        for j, s in enumerate(segs_order):
            matrix[i][j] = counts.get((r, s), 0)
    filled = int(np.sum(matrix > 0))

    fig = plt.figure(figsize=(20, 13))
    fig.patch.set_facecolor(C_BG)

    # 헤드라인
    fig.text(0.5, 0.96, "AI 페르소나 생성 시스템",
             ha="center", fontsize=28, fontweight="bold", color=C_TITLE)
    fig.text(0.5, 0.935,
             "직업 · 성격 · 디지털 숙련도 · 예산 민감도를 조합해 실제 사용자 분포를 재현합니다",
             ha="center", fontsize=13, color=C_SUB)

    # --- KPI 카드 3개 ---
    kpis = [
        ("30", "명", "AI 페르소나", "Big Five 성격 모델 기반 생성"),
        ("6 × 10", "", "직업 × 성격 조합", f"60가지 중 {filled}가지 활성"),
        ("97", "건", "실제 G2 리뷰", "비교 검증용 벤치마크 데이터"),
    ]
    for i, (num, unit, title, desc) in enumerate(kpis):
        cx = 0.11 + i * 0.145
        # 카드 배경
        card = FancyBboxPatch((cx - 0.055, 0.855), 0.125, 0.065,
                              boxstyle="round,pad=0.008",
                              facecolor=C_CARD, edgecolor="#E5E7EB", linewidth=1,
                              transform=fig.transFigure)
        fig.patches.append(card)

        fig.text(cx, 0.895, f"{num}{unit}", fontsize=26, fontweight="bold",
                 color=C_ACCENT, ha="center")
        fig.text(cx, 0.875, title, fontsize=10, fontweight="bold",
                 color=C_TITLE, ha="center")
        fig.text(cx, 0.86, desc, fontsize=8, color=C_SUB, ha="center")

    # --- Big Five 레이더 (우측) ---
    ax_radar = fig.add_axes([0.68, 0.82, 0.28, 0.16], polar=True)
    ax_radar.set_facecolor("none")

    seg_data = defaultdict(list)
    for p in personas:
        seg_data[p["segment"]].append([p["big_five"][k] for k in BIG_FIVE_KEYS])

    highlight = [("anxious", C_RED, "불안형"), ("explorer", C_TEAL, "탐험형"),
                 ("power_user", "#2C3E50", "파워유저")]
    angles = np.linspace(0, 2 * np.pi, 5, endpoint=False).tolist() + [0]

    for seg, color, label in highlight:
        if seg in seg_data:
            vals = np.mean(seg_data[seg], axis=0).tolist() + [np.mean(seg_data[seg], axis=0)[0]]
            ax_radar.fill(angles, vals, alpha=0.2, color=color)
            ax_radar.plot(angles, vals, "o-", color=color, linewidth=2.5,
                         markersize=5, label=label)

    ax_radar.set_ylim(0, 1)
    ax_radar.set_yticks([])
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(BIG_FIVE_KR, fontsize=8, color=C_SUB)
    ax_radar.grid(color="#E5E7EB", linewidth=0.5)
    ax_radar.spines["polar"].set_visible(False)
    ax_radar.legend(loc="upper left", bbox_to_anchor=(-0.15, 1.25),
                    fontsize=8, frameon=False, ncol=3)
    fig.text(0.82, 0.985, "성격 유형별 Big Five 프로필",
             ha="center", fontsize=10, fontweight="bold", color=C_TITLE)

    # --- 매트릭스 ---
    ax = fig.add_axes([0.04, 0.03, 0.92, 0.78])
    ax.set_facecolor(C_BG)
    ax.axis("off")

    n_rows, n_cols = len(roles_order), len(segs_order)
    x_offset = 0.16
    y_offset = 0.92
    cell_w = (0.82) / n_cols
    cell_h = 0.13

    # 매트릭스 제목
    ax.text(0.5, 0.99, "직업군 × 행동 유형 생성 매트릭스",
            ha="center", fontsize=15, fontweight="bold", color=C_TITLE,
            transform=ax.transAxes)
    ax.text(0.5, 0.965,
            "실제 G2 리뷰어 직업 분포 반영  ·  빈 칸 = 현실에서 드문 조합",
            ha="center", fontsize=9, color=C_SUB, transform=ax.transAxes)

    # 열 헤더
    for j, seg in enumerate(segs_order):
        x = x_offset + (j + 0.5) * cell_w
        ax.text(x, y_offset + 0.01, SEGMENT_KR[seg],
                ha="center", va="bottom", fontsize=9.5, color=C_SUB, fontweight="bold",
                transform=ax.transAxes)

    # 행
    for i, role in enumerate(roles_order):
        y = y_offset - (i + 1) * cell_h
        # 역할 레이블
        ax.text(x_offset - 0.01, y + cell_h * 0.5, ROLE_KR[role],
                ha="right", va="center", fontsize=11, fontweight="bold", color=C_TITLE,
                transform=ax.transAxes)

        row_total = int(matrix[i].sum())

        for j, seg in enumerate(segs_order):
            val = int(matrix[i][j])
            x = x_offset + j * cell_w
            pad = 0.006

            if val > 0:
                alpha = 0.35 + val * 0.2
                rect = FancyBboxPatch(
                    (x + pad, y + pad), cell_w - 2*pad, cell_h - 2*pad,
                    boxstyle="round,pad=0.008",
                    facecolor=(*matplotlib.colors.to_rgb(C_ACCENT), min(alpha, 0.95)),
                    edgecolor="white", linewidth=1,
                    transform=ax.transAxes)
                ax.add_patch(rect)
                ax.text(x + cell_w/2, y + cell_h/2, str(val),
                        ha="center", va="center", fontsize=16, fontweight="bold",
                        color="white", transform=ax.transAxes)
            else:
                rect = FancyBboxPatch(
                    (x + pad, y + pad), cell_w - 2*pad, cell_h - 2*pad,
                    boxstyle="round,pad=0.008",
                    facecolor="#F3F4F6", edgecolor="#E5E7EB", linewidth=0.5,
                    transform=ax.transAxes)
                ax.add_patch(rect)

        # 행 합계
        ax.text(x_offset + n_cols * cell_w + 0.015, y + cell_h/2,
                f"{row_total}명", ha="left", va="center",
                fontsize=12, fontweight="bold", color=C_ACCENT,
                transform=ax.transAxes)

    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  Saved: {out}")


# ============================================================
def main():
    base = Path(__file__).resolve().parent.parent
    personas = load_personas(base / "configs" / "personas" / "benchmark")
    out = base / "docs" / "charts"
    out.mkdir(parents=True, exist_ok=True)

    print(f"Loaded {len(personas)} personas")
    print(f"Font: {setup_korean_font()}")

    chart_persona_comparison(personas, out / "persona_comparison.png")
    chart_system_overview(personas, out / "persona_system_overview.png")
    print("Done!")


if __name__ == "__main__":
    main()
