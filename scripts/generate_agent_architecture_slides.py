#!/usr/bin/env python3
"""Personica Agent 아키텍처 2장 슬라이드 생성기.

PPT에 바로 넣을 수 있는 16:9 비주얼을 PNG / SVG로 생성한다.
"""

from __future__ import annotations

import os
from pathlib import Path

# matplotlib 캐시 경로를 writable 영역으로 고정한다.
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as fm
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "charts"


BG = "#F5F1E8"
TEXT = "#162338"
MUTED = "#5F6B7A"
LINE = "#D9E0EA"
NAVY = "#22446B"
TEAL = "#2D8F85"
CORAL = "#DB6B4D"
AMBER = "#F2A65A"
WHITE = "#FFFFFF"
SOFT_BLUE = "#EEF5FB"
SOFT_ORANGE = "#FFF2E8"
SOFT_GREEN = "#EDF7F5"
SOFT_GRAY = "#F8FAFC"
RISK = "#C75A4A"


def setup_korean_font() -> str:
    """세션에서 사용할 한글 폰트를 선택한다."""
    candidates = [
        "NanumSquare",
        "NanumGothic",
        "NanumBarunGothic",
        "Noto Sans CJK KR",
        "DejaVu Sans",
    ]
    available = {font.name for font in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            plt.rcParams["axes.unicode_minus"] = False
            return name
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False
    return "DejaVu Sans"


def make_canvas() -> tuple[plt.Figure, plt.Axes]:
    """슬라이드용 16:9 캔버스를 만든다."""
    fig = plt.figure(figsize=(13.333, 7.5), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    return fig, ax


def add_shadow(patch: FancyBboxPatch) -> None:
    """박스에 은은한 그림자를 준다."""
    patch.set_path_effects(
        [
            pe.withSimplePatchShadow(offset=(0.12, -0.12), shadow_rgbFace="#D7D1C8", alpha=0.35),
            pe.Normal(),
        ]
    )


def add_box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body: str = "",
    *,
    fill: str = WHITE,
    edge: str = LINE,
    accent: str = NAVY,
    title_color: str = TEXT,
    body_color: str = MUTED,
    title_size: float = 13,
    body_size: float = 9.2,
    align: str = "left",
    tag: str | None = None,
) -> None:
    """라운드 박스를 그리고 텍스트를 배치한다."""
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.03,rounding_size=0.18",
        linewidth=1.8,
        edgecolor=edge,
        facecolor=fill,
    )
    add_shadow(patch)
    ax.add_patch(patch)

    accent_bar = FancyBboxPatch(
        (x + 0.12, y + h - 0.18),
        w - 0.24,
        0.10,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=0,
        facecolor=accent,
    )
    ax.add_patch(accent_bar)

    if tag:
        tag_width = min(0.17 * len(tag) + 0.55, max(w - 0.42, 1.1))
        tag_patch = FancyBboxPatch(
            (x + w - tag_width - 0.18, y + h - 0.54),
            tag_width,
            0.28,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=0,
            facecolor=accent,
        )
        ax.add_patch(tag_patch)
        ax.text(
            x + w - tag_width / 2 - 0.18,
            y + h - 0.40,
            tag,
            ha="center",
            va="center",
            fontsize=7.0,
            color=WHITE,
            fontweight="bold",
        )

    title_x = x + 0.22 if align == "left" else x + w / 2
    body_x = x + 0.22 if align == "left" else x + w / 2
    ha = "left" if align == "left" else "center"

    ax.text(
        title_x,
        y + h - 0.34,
        title,
        ha=ha,
        va="top",
        fontsize=title_size,
        color=title_color,
        fontweight="bold",
    )
    if body:
        ax.text(
            body_x,
            y + h - 0.82,
            body,
            ha=ha,
            va="top",
            fontsize=body_size,
            color=body_color,
            linespacing=1.45,
        )


def add_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = NAVY,
    width: float = 2.0,
    style: str = "-|>",
    curve: float = 0.0,
    linestyle: str = "-",
    zorder: int = 3,
) -> None:
    """모듈 간 흐름 화살표."""
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle=style,
        mutation_scale=15,
        linewidth=width,
        color=color,
        connectionstyle=f"arc3,rad={curve}",
        linestyle=linestyle,
        zorder=zorder,
    )
    ax.add_patch(arrow)


def add_step(ax: plt.Axes, x: float, y: float, text: str, *, fill: str = NAVY) -> None:
    """흐름 단계용 캡슐."""
    width = 0.17 * len(text) + 0.55
    patch = FancyBboxPatch(
        (x - width / 2, y - 0.14),
        width,
        0.30,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=0,
        facecolor=fill,
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=7.6, color=WHITE, fontweight="bold")


def add_chip(
    ax: plt.Axes,
    x: float,
    y: float,
    text: str,
    *,
    fill: str,
    edge: str,
    text_color: str = TEXT,
    width: float | None = None,
) -> None:
    """하단 요약용 칩."""
    chip_width = width if width is not None else 0.18 * len(text) + 0.7
    patch = FancyBboxPatch(
        (x - chip_width / 2, y - 0.18),
        chip_width,
        0.36,
        boxstyle="round,pad=0.02,rounding_size=0.14",
        linewidth=1.2,
        edgecolor=edge,
        facecolor=fill,
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=8.3, color=text_color, fontweight="bold")


def add_number_badge(ax: plt.Axes, x: float, y: float, number: str, fill: str) -> None:
    """번호 원형 배지."""
    circle = Circle((x, y), radius=0.14, facecolor=fill, edgecolor="none", zorder=5)
    ax.add_patch(circle)
    ax.text(x, y, number, ha="center", va="center", fontsize=8.2, color=WHITE, fontweight="bold", zorder=6)


def draw_slide_1() -> plt.Figure:
    """슬라이드 1: Personica Agent 전체 구조."""
    fig, ax = make_canvas()

    ax.text(
        0.85,
        8.66,
        "Personica Agent Architecture",
        fontsize=26,
        fontweight="bold",
        color=TEXT,
        zorder=20,
    )
    ax.text(
        0.86,
        8.28,
        "표준 AI Agent 뼈대 위에 Profile + Emotion & Cognition Engine을 추가해"
        " 사람처럼 다른 반응을 만드는 구조",
        fontsize=12.5,
        color=MUTED,
        zorder=20,
    )

    add_chip(ax, 12.65, 8.42, "표준 Agent 모듈", fill=SOFT_BLUE, edge="#BCD1E5", width=1.75)
    add_chip(ax, 14.45, 8.42, "Personica 전용 모듈", fill=SOFT_ORANGE, edge="#F0B37E", width=2.20)

    add_box(
        ax,
        0.65,
        7.00,
        14.7,
        0.68,
        "Environment  |  실제 웹/앱 (브라우저 · 모바일 웹 · SaaS 화면)",
        "",
        fill=NAVY,
        edge=NAVY,
        accent=TEAL,
        title_color=WHITE,
        align="center",
        title_size=14,
    )

    outer = FancyBboxPatch(
        (0.55, 0.92),
        14.9,
        5.88,
        boxstyle="round,pad=0.03,rounding_size=0.22",
        linewidth=2.0,
        edgecolor="#D4C9B7",
        facecolor="#FFFDFC",
    )
    add_shadow(outer)
    ax.add_patch(outer)
    ax.text(0.86, 6.60, "Persona Agent", fontsize=13.5, color=TEXT, fontweight="bold")

    add_box(
        ax,
        0.95,
        5.58,
        3.10,
        1.00,
        "Perception",
        "브라우저 접근성 스냅샷 수신\n화면 구조 · 요소 · 상태 파싱",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=NAVY,
        body_size=8.9,
    )
    add_box(
        ax,
        0.95,
        4.08,
        3.10,
        1.15,
        "Profile",
        "Big Five → 행동 파라미터\n디지털 숙련도 · JTBD · 인구통계",
        fill=SOFT_ORANGE,
        edge="#F0B37E",
        accent=CORAL,
        body_size=8.9,
    )
    add_box(
        ax,
        4.55,
        4.18,
        5.20,
        2.40,
        "Brain (LLM)",
        "화면 해석  ·  1인칭 사고  ·  행동 의도 생성\n"
        "예: \"이 버튼이 뭐지?\"  \"찾던 기능인데...\"  \"가입 버튼을 눌러보자\"\n\n"
        "감정 상태는 외부 엔진이 계산해 주입",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=NAVY,
        body_size=9.2,
    )
    add_box(
        ax,
        4.75,
        2.48,
        2.05,
        1.20,
        "Planning",
        "목표 분해\n다음 스텝 결정",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=TEAL,
        body_size=8.8,
    )
    add_box(
        ax,
        7.25,
        2.18,
        2.95,
        1.60,
        "Emotion & Cognition",
        "인지부하 · 기대 괴리\nOCC → PAD → SDE\nFogg 체크 · 만족 판정\n이탈 임계치 계산",
        fill=SOFT_ORANGE,
        edge="#F0B37E",
        accent=CORAL,
        body_size=8.4,
    )
    add_box(
        ax,
        10.75,
        3.05,
        3.75,
        1.28,
        "Tools",
        "click(target)  ·  type(text)\nscroll()  ·  back()  ·  abandon()",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=TEAL,
        body_size=8.8,
    )
    add_box(
        ax,
        1.00,
        1.05,
        13.50,
        0.92,
        "Memory",
        "단기: 현재 세션 행동 로그 · 감정 궤적   |   장기: 기억 스트림 · 반추 · 습관 강도 · 만족 추이",
        fill=SOFT_GREEN,
        edge="#B7DDD7",
        accent=TEAL,
        body_size=8.7,
    )

    add_arrow(ax, (2.50, 6.98), (2.50, 6.62), color=NAVY, width=2.3)
    add_arrow(ax, (4.05, 6.05), (4.55, 6.05), color=NAVY, width=2.1)
    add_arrow(ax, (4.05, 4.65), (4.55, 4.65), color=CORAL, width=2.1)
    add_arrow(ax, (7.10, 4.18), (5.95, 3.68), color=NAVY, width=2.1, curve=0.08)
    add_arrow(ax, (8.75, 4.18), (8.75, 3.80), color=CORAL, width=2.1)
    add_arrow(ax, (9.70, 3.80), (9.15, 4.18), color=CORAL, width=2.3, curve=-0.20)
    add_arrow(ax, (6.80, 3.08), (10.75, 3.68), color=NAVY, width=2.1)
    add_arrow(ax, (12.65, 4.33), (12.65, 6.98), color=TEAL, width=2.3)
    add_arrow(ax, (12.65, 3.05), (12.65, 1.97), color=TEAL, width=2.0)
    add_arrow(ax, (8.70, 2.18), (8.70, 1.97), color=CORAL, width=2.0)
    add_arrow(ax, (8.10, 1.97), (8.10, 4.18), color=TEAL, width=1.7, curve=-0.18, linestyle="--")

    add_number_badge(ax, 2.12, 6.68, "1", NAVY)
    ax.text(2.33, 6.68, "Observe", fontsize=8.5, color=NAVY, va="center", fontweight="bold")

    add_number_badge(ax, 4.30, 4.97, "2", CORAL)
    ax.text(4.52, 4.97, "성격 파라미터", fontsize=8.2, color=CORAL, va="center", fontweight="bold")

    add_number_badge(ax, 6.00, 3.92, "3", NAVY)
    ax.text(6.22, 3.92, "Think", fontsize=8.2, color=NAVY, va="center", fontweight="bold")

    add_number_badge(ax, 9.95, 4.35, "4", CORAL)
    ax.text(10.18, 4.35, "감정 · 인지 상태 주입", fontsize=8.2, color=CORAL, va="center", fontweight="bold")

    add_number_badge(ax, 8.15, 3.18, "5", TEAL)
    ax.text(8.37, 3.18, "Plan", fontsize=8.2, color=TEAL, va="center", fontweight="bold")

    add_number_badge(ax, 12.92, 6.68, "6", TEAL)
    ax.text(13.14, 6.68, "Act", fontsize=8.2, color=TEAL, va="center", fontweight="bold")

    add_step(ax, 3.55, 0.42, "Observe → Perceive", fill=NAVY)
    add_step(ax, 7.10, 0.42, "Think (+ Emotion)", fill=CORAL)
    add_step(ax, 10.10, 0.42, "Plan → Act", fill=TEAL)
    add_step(ax, 13.35, 0.42, "Log to Memory", fill="#567C79")

    return fig


def draw_slide_2() -> plt.Figure:
    """슬라이드 2: 일반 Agent vs Personica Agent 비교."""
    fig, ax = make_canvas()

    fig.text(
        0.06,
        0.93,
        "General AI Agent vs Personica Agent",
        fontsize=26,
        fontweight="bold",
        color=TEXT,
    )
    fig.text(
        0.06,
        0.885,
        "차이는 뼈대가 아니라 감정·인지 계산 위치다. Personica는 감정을 LLM이 직접 꾸미지 않게 만든다.",
        fontsize=12.5,
        color=MUTED,
    )

    left_card = FancyBboxPatch(
        (0.70, 1.15),
        6.45,
        6.10,
        boxstyle="round,pad=0.03,rounding_size=0.24",
        linewidth=1.8,
        edgecolor="#CBD5E1",
        facecolor="#FCFDFE",
    )
    add_shadow(left_card)
    ax.add_patch(left_card)

    right_card = FancyBboxPatch(
        (8.85, 1.15),
        6.45,
        6.10,
        boxstyle="round,pad=0.03,rounding_size=0.24",
        linewidth=2.0,
        edgecolor="#E8B07B",
        facecolor="#FFFDFC",
    )
    add_shadow(right_card)
    ax.add_patch(right_card)

    ax.text(1.00, 6.92, "일반 AI Agent", fontsize=17, fontweight="bold", color=TEXT)
    ax.text(1.00, 6.63, "감정도 Brain(LLM) 내부에서 직접 판단", fontsize=10, color=MUTED)
    ax.text(9.15, 6.92, "Personica Agent", fontsize=17, fontweight="bold", color=TEXT)
    ax.text(9.15, 6.63, "표준 Agent 위에 Profile + Emotion Engine 추가", fontsize=10, color=MUTED)

    # 좌측 스택
    add_box(
        ax,
        1.15,
        5.72,
        5.55,
        0.72,
        "Perception",
        "화면/입력 수신",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=NAVY,
        body_size=8.6,
    )
    add_box(
        ax,
        1.15,
        4.32,
        5.55,
        1.12,
        "Brain (LLM)",
        "해석 · 판단 · 1인칭 사고\n감정도 이 안에서 직접 판단",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=NAVY,
        body_size=9.0,
    )
    add_box(
        ax,
        1.15,
        3.14,
        5.55,
        0.82,
        "Planning",
        "다음 행동 결정",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=TEAL,
        body_size=8.7,
    )
    add_box(
        ax,
        1.15,
        1.97,
        5.55,
        0.86,
        "Tools → Action",
        "브라우저 조작 · 실행",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=TEAL,
        body_size=8.7,
    )
    add_box(
        ax,
        1.15,
        1.18,
        5.55,
        0.70,
        "Memory",
        "로그/히스토리 보관",
        fill=SOFT_GREEN,
        edge="#B7DDD7",
        accent=TEAL,
        body_size=8.5,
    )

    add_arrow(ax, (3.93, 5.72), (3.93, 5.44), color=NAVY, width=1.9)
    add_arrow(ax, (3.93, 4.32), (3.93, 3.96), color=NAVY, width=1.9)
    add_arrow(ax, (3.93, 3.14), (3.93, 2.83), color=TEAL, width=1.9)
    add_arrow(ax, (3.93, 1.97), (3.93, 1.88), color=TEAL, width=1.9)

    # 우측 스택
    add_box(
        ax,
        9.25,
        5.88,
        2.35,
        0.72,
        "Perception",
        "화면/입력 수신",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=NAVY,
        body_size=8.4,
    )
    add_box(
        ax,
        9.25,
        4.78,
        2.35,
        0.82,
        "Profile",
        "Big Five → 행동 파라미터",
        fill=SOFT_ORANGE,
        edge="#F0B37E",
        accent=CORAL,
        body_size=8.3,
    )
    add_box(
        ax,
        12.00,
        4.58,
        2.60,
        1.22,
        "Brain (LLM)",
        "해석 · 사고\n행동 의도 생성",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=NAVY,
        body_size=8.9,
    )
    add_box(
        ax,
        9.25,
        3.00,
        2.35,
        1.05,
        "Planning",
        "목표 분해\n다음 스텝 결정",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=TEAL,
        body_size=8.5,
    )
    add_box(
        ax,
        12.05,
        2.82,
        2.75,
        1.42,
        "Emotion & Cognition",
        "OCC → PAD → SDE\n인지부하 · Fogg 체크\n감정 상태를 계산 후 주입",
        fill=SOFT_ORANGE,
        edge="#F0B37E",
        accent=CORAL,
        body_size=8.2,
    )
    add_box(
        ax,
        9.25,
        1.82,
        5.55,
        0.84,
        "Tools → Action",
        "실제 브라우저 조작 · 포기/이탈까지 포함",
        fill=SOFT_BLUE,
        edge="#BCD1E5",
        accent=TEAL,
        body_size=8.6,
    )
    add_box(
        ax,
        9.25,
        1.05,
        5.55,
        0.70,
        "Memory",
        "행동 로그 · 감정 궤적 · 장기 기억",
        fill=SOFT_GREEN,
        edge="#B7DDD7",
        accent=TEAL,
        body_size=8.5,
    )

    add_arrow(ax, (11.60, 6.24), (12.00, 5.52), color=NAVY, width=1.9)
    add_arrow(ax, (11.60, 5.19), (12.00, 5.19), color=CORAL, width=1.9)
    add_arrow(ax, (13.20, 4.58), (10.42, 4.05), color=NAVY, width=1.9, curve=0.06)
    add_arrow(ax, (13.40, 4.58), (13.42, 4.24), color=CORAL, width=2.0)
    add_arrow(ax, (12.10, 4.05), (12.88, 4.58), color=CORAL, width=2.1, curve=-0.16)
    add_arrow(ax, (10.42, 3.00), (10.42, 2.66), color=TEAL, width=1.9)
    add_arrow(ax, (12.10, 2.82), (12.10, 2.66), color=CORAL, width=1.9)
    add_arrow(ax, (12.03, 1.82), (12.03, 1.75), color=TEAL, width=1.9)

    add_chip(ax, 12.00, 8.06, "같은 표준 Agent 뼈대", fill=SOFT_BLUE, edge="#BCD1E5", width=2.25)
    add_chip(ax, 14.28, 8.06, "차이는 감정 계산 위치", fill=SOFT_ORANGE, edge="#F0B37E", width=2.65)

    add_box(
        ax,
        1.15,
        0.30,
        5.55,
        0.56,
        "감정 = LLM 직접 판단  |  긍정 편향 노출  |  페르소나 분화 약함",
        "",
        fill="#FCEBE6",
        edge="#E2B5AA",
        accent=RISK,
        title_color=RISK,
        title_size=9.8,
        align="center",
    )
    add_box(
        ax,
        9.25,
        0.30,
        5.55,
        0.56,
        "감정 = 수학 계산 후 LLM에 주입  |  긍정 편향 구조적 완화  |  페르소나별 다른 반응",
        "",
        fill="#FFF2E8",
        edge="#F0B37E",
        accent=CORAL,
        title_color=CORAL,
        title_size=9.2,
        align="center",
    )

    return fig


def save_figure(fig: plt.Figure, stem: str) -> None:
    """PNG와 SVG를 함께 저장한다."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUT_DIR / f"{stem}.png"
    svg_path = OUT_DIR / f"{stem}.svg"
    fig.savefig(png_path, dpi=180, facecolor=BG)
    fig.savefig(svg_path, facecolor=BG)
    plt.close(fig)
    print(f"saved {png_path.relative_to(ROOT)}")
    print(f"saved {svg_path.relative_to(ROOT)}")


def main() -> None:
    font_name = setup_korean_font()
    print(f"font={font_name}")
    save_figure(draw_slide_1(), "personica_agent_architecture_slide_1")
    save_figure(draw_slide_2(), "personica_agent_architecture_slide_2")


if __name__ == "__main__":
    main()
