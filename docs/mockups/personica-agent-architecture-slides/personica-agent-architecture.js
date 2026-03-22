"use strict";

const path = require("path");
const PptxGenJS = require("pptxgenjs");
const {
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require("./pptxgenjs_helpers/layout");
const { safeOuterShadow } = require("./pptxgenjs_helpers/util");

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "OpenAI Codex";
pptx.company = "Personica";
pptx.subject = "Personica Agent Architecture";
pptx.title = "Personica Agent Architecture";
pptx.lang = "ko-KR";
pptx.theme = {
  headFontFace: "NanumSquare",
  bodyFontFace: "Noto Sans CJK KR",
  lang: "ko-KR",
};

const OUT_PATH = path.join(__dirname, "personica-agent-architecture.pptx");

const C = {
  bg: "F5F7FB",
  ink: "102033",
  muted: "607089",
  navy: "102A43",
  blue: "2563EB",
  blueSoft: "E8F0FF",
  blueBorder: "B8CCFF",
  teal: "0F766E",
  tealSoft: "DFF7F4",
  orange: "C2410C",
  orangeSoft: "FFF0E5",
  orangeBorder: "FDBA8C",
  gold: "D97706",
  goldSoft: "FFF7D6",
  rose: "BE123C",
  roseSoft: "FFE3EA",
  green: "0F766E",
  greenSoft: "DCFCE7",
  red: "B42318",
  redSoft: "FEE4E2",
  grayCard: "FFFFFF",
  grayBorder: "D7DFEA",
  graySoft: "EEF2F8",
  line: "7C8AA5",
};

function addSlideBase(slide, title, subtitle) {
  slide.background = { color: C.bg };
  slide.addText(title, {
    x: 0.62,
    y: 0.34,
    w: 7.3,
    h: 0.38,
    fontFace: "NanumSquare",
    fontSize: 23,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  slide.addText(subtitle, {
    x: 0.64,
    y: 0.78,
    w: 9.8,
    h: 0.28,
    fontFace: "Noto Sans CJK KR",
    fontSize: 10.5,
    color: C.muted,
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.62,
    y: 1.1,
    w: 12.1,
    h: 0,
    line: { color: "DCE4EF", width: 1.1 },
  });
}

function addTag(slide, text, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: opts.x,
    y: opts.y,
    w: opts.w,
    h: opts.h,
    rectRadius: 0.06,
    fill: { color: opts.fill || C.blueSoft },
    line: { color: opts.line || opts.fill || C.blueSoft, width: 0.8 },
  });
  slide.addText(text, {
    x: opts.x + 0.08,
    y: opts.y + 0.03,
    w: opts.w - 0.16,
    h: opts.h - 0.06,
    align: "center",
    valign: "mid",
    fontFace: "Noto Sans CJK KR",
    fontSize: opts.fontSize || 8,
    bold: true,
    color: opts.color || C.blue,
    margin: 0,
  });
}

function addCard(slide, cfg) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: cfg.x,
    y: cfg.y,
    w: cfg.w,
    h: cfg.h,
    rectRadius: 0.08,
    fill: { color: cfg.fill || C.grayCard },
    line: { color: cfg.line || C.grayBorder, width: cfg.lineWidth || 1.4 },
    shadow: cfg.shadow === false ? undefined : safeOuterShadow("93A4BF", 0.12, 45, 2, 1),
  });

  if (cfg.kicker) {
    addTag(slide, cfg.kicker, {
      x: cfg.x + 0.14,
      y: cfg.y + 0.12,
      w: Math.min(cfg.w - 0.28, cfg.kickerWidth || 1.15),
      h: 0.24,
      fill: cfg.kickerFill || C.blueSoft,
      line: cfg.kickerFill || C.blueSoft,
      color: cfg.kickerColor || C.blue,
      fontSize: 7.2,
    });
  }

  slide.addText(cfg.title, {
    x: cfg.x + 0.16,
    y: cfg.y + (cfg.kicker ? 0.42 : 0.16),
    w: cfg.w - 0.32,
    h: cfg.titleH ?? 0.28,
    fontFace: cfg.titleFont || "NanumSquare",
    fontSize: cfg.titleSize || 13.5,
    bold: true,
    color: cfg.titleColor || C.ink,
    margin: 0,
    align: cfg.align || "left",
  });

  if (cfg.body) {
    slide.addText(cfg.body, {
      x: cfg.x + 0.16,
      y: cfg.y + (cfg.bodyY ?? (cfg.kicker ? 0.76 : 0.5)),
      w: cfg.w - 0.32,
      h: cfg.bodyH ?? (cfg.h - (cfg.kicker ? 0.9 : 0.66)),
      fontFace: "Noto Sans CJK KR",
      fontSize: cfg.bodySize || 8.6,
      color: cfg.bodyColor || C.muted,
      margin: 0,
      breakLine: false,
      valign: "top",
      align: cfg.align || "left",
    });
  }
}

function addArrow(slide, cfg) {
  slide.addShape(pptx.ShapeType.line, {
    x: cfg.x1,
    y: cfg.y1,
    w: cfg.x2 - cfg.x1,
    h: cfg.y2 - cfg.y1,
    line: {
      color: cfg.color || C.line,
      width: cfg.width || 1.6,
      beginArrowType: cfg.beginArrow ? "triangle" : "none",
      endArrowType: cfg.endArrow === false ? "none" : "triangle",
      dash: cfg.dash || "solid",
    },
  });

  if (cfg.label) {
    slide.addText(cfg.label, {
      x: cfg.lx,
      y: cfg.ly,
      w: cfg.lw || 1.3,
      h: cfg.lh || 0.22,
      fontFace: "Noto Sans CJK KR",
      fontSize: cfg.labelSize || 7.4,
      color: cfg.labelColor || C.muted,
      bold: cfg.labelBold || false,
      margin: 0,
      align: cfg.labelAlign || "center",
    });
  }
}

function addLoopPill(slide, x, y, w, text, fill, color) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h: 0.26,
    rectRadius: 0.08,
    fill: { color: fill },
    line: { color: fill, width: 0.8 },
  });
  slide.addText(text, {
    x,
    y: y + 0.03,
    w,
    h: 0.18,
    align: "center",
    fontFace: "Noto Sans CJK KR",
    fontSize: 7.4,
    bold: true,
    color,
    margin: 0,
  });
}

function addChevronText(slide, x, y, text) {
  slide.addText(text, {
    x,
    y,
    w: 0.3,
    h: 0.18,
    align: "center",
    fontFace: "NanumSquare",
    fontSize: 9,
    color: C.muted,
    margin: 0,
  });
}

function addStepBadge(slide, x, y, n) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x,
    y,
    w: 0.24,
    h: 0.24,
    fill: { color: C.navy },
    line: { color: C.navy, width: 0.8 },
  });
  slide.addText(String(n), {
    x,
    y: y + 0.025,
    w: 0.24,
    h: 0.16,
    align: "center",
    fontFace: "NanumSquare",
    fontSize: 8,
    bold: true,
    color: "FFFFFF",
    margin: 0,
  });
}

function addFooterNote(slide, text, x, y, w) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h: 0.5,
    rectRadius: 0.08,
    fill: { color: C.goldSoft },
    line: { color: "F5D26A", width: 0.9 },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: x + 0.12,
    y: y + 0.08,
    w: 0.24,
    h: 0.24,
    fill: { color: "FFF7D6" },
    line: { color: "F5C451", width: 0.9 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: x + 0.24,
    y: y + 0.13,
    w: 0,
    h: 0.09,
    line: {
      color: "B45309",
      width: 1.2,
      beginArrowType: "none",
      endArrowType: "none",
    },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: x + 0.215,
    y: y + 0.255,
    w: 0.05,
    h: 0.05,
    fill: { color: "B45309" },
    line: { color: "B45309", width: 0.6 },
  });
  slide.addText(text, {
    x: x + 0.42,
    y: y + 0.1,
    w: w - 0.54,
    h: 0.22,
    fontFace: "Noto Sans CJK KR",
    fontSize: 8.2,
    color: C.gold,
    bold: true,
    margin: 0,
  });
}

function buildArchitectureSlide() {
  const slide = pptx.addSlide();
  addSlideBase(
    slide,
    "Personica Agent Architecture",
    "표준 AI Agent 프레임에 Profile과 Emotion & Cognition Engine이 추가되어, 감정 판단을 LLM 바깥의 구조화된 계산으로 분리합니다."
  );

  addLoopPill(slide, 8.85, 0.38, 0.9, "Observe", C.blueSoft, C.blue);
  addChevronText(slide, 9.77, 0.42, ">");
  addLoopPill(slide, 10.05, 0.38, 0.92, "Think", C.orangeSoft, C.orange);
  addChevronText(slide, 11.01, 0.42, ">");
  addLoopPill(slide, 11.3, 0.38, 0.82, "Plan", C.blueSoft, C.blue);
  addChevronText(slide, 12.13, 0.42, ">");
  addLoopPill(slide, 12.38, 0.38, 0.52, "Act", C.tealSoft, C.teal);

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.82,
    y: 1.38,
    w: 11.7,
    h: 0.58,
    rectRadius: 0.08,
    fill: { color: C.navy },
    line: { color: C.navy, width: 1 },
  });
  addTag(slide, "ENVIRONMENT", {
    x: 1.02,
    y: 1.55,
    w: 1.1,
    h: 0.22,
    fill: "1F4068",
    line: "1F4068",
    color: "D9E9FF",
    fontSize: 7.2,
  });
  slide.addText("실제 웹/앱 (브라우저)", {
    x: 2.35,
    y: 1.55,
    w: 4.0,
    h: 0.2,
    fontFace: "Noto Sans CJK KR",
    fontSize: 16,
    bold: true,
    color: "FFFFFF",
    margin: 0,
  });

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.74,
    y: 2.18,
    w: 11.9,
    h: 4.68,
    rectRadius: 0.12,
    fill: { color: "FCFDFE", transparency: 2 },
    line: { color: C.grayBorder, width: 1.4 },
  });
  addTag(slide, "PERSONA AGENT", {
    x: 0.96,
    y: 2.03,
    w: 1.38,
    h: 0.28,
    fill: C.graySoft,
    line: C.graySoft,
    color: C.muted,
    fontSize: 7.4,
  });

  addCard(slide, {
    x: 1.0,
    y: 2.52,
    w: 2.22,
    h: 0.98,
    fill: C.blueSoft,
    line: C.blueBorder,
    kicker: "STANDARD",
    title: "Perception",
    body: "브라우저 접근성 스냅샷 수신 · 파싱",
    titleColor: C.blue,
    bodyColor: "35506A",
    kickerWidth: 0.95,
  });

  addCard(slide, {
    x: 1.0,
    y: 3.78,
    w: 2.22,
    h: 1.14,
    fill: C.orangeSoft,
    line: C.orangeBorder,
    kicker: "PERSONICA ONLY",
    kickerFill: "FFE2D0",
    kickerColor: C.orange,
    kickerWidth: 1.42,
    title: "Profile",
    body: "Big Five 성격 → 행동 파라미터\n디지털 숙련도 · JTBD · 인구통계",
    titleColor: C.orange,
    bodyColor: "7A3B14",
  });

  addCard(slide, {
    x: 3.6,
    y: 2.42,
    w: 3.46,
    h: 1.78,
    fill: C.grayCard,
    line: C.grayBorder,
    kicker: "STANDARD",
    title: "Brain (LLM)",
    body: "화면 해석\n1인칭 사고\n행동 의도 생성",
    titleSize: 15,
    bodyY: 3.14 - 2.42,
    bodyH: 0.42,
    bodySize: 8.2,
    titleColor: C.ink,
    bodyColor: "43536A",
    kickerWidth: 0.95,
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 3.88,
    y: 3.66,
    w: 2.94,
    h: 0.38,
    rectRadius: 0.06,
    fill: { color: C.roseSoft },
    line: { color: "F9C7D6", width: 0.8 },
  });
  slide.addText("감정 상태를 외부에서 주입받음", {
    x: 4.05,
    y: 3.67,
    w: 2.62,
    h: 0.13,
    fontFace: "Noto Sans CJK KR",
    fontSize: 7.8,
    bold: true,
    color: C.rose,
    margin: 0,
    align: "center",
  });

  addCard(slide, {
    x: 7.46,
    y: 2.56,
    w: 2.06,
    h: 1.06,
    fill: C.blueSoft,
    line: C.blueBorder,
    kicker: "STANDARD",
    title: "Planning",
    body: "목표 분해\n다음 스텝 결정",
    titleColor: C.blue,
    bodyColor: "35506A",
    kickerWidth: 0.95,
  });

  addCard(slide, {
    x: 4.0,
    y: 4.56,
    w: 4.88,
    h: 1.42,
    fill: C.orangeSoft,
    line: C.orangeBorder,
    kicker: "PERSONICA ONLY",
    kickerFill: "FFE2D0",
    kickerColor: C.orange,
    kickerWidth: 1.42,
    title: "Emotion & Cognition Engine",
    body: "인지: 인지부하 · 기대 괴리\n감정: OCC → PAD → SDE\n판단: Fogg 체크 · 만족 판정 · 이탈 임계치",
    titleColor: C.orange,
    bodyColor: "7A3B14",
    titleSize: 14.4,
    bodySize: 8.2,
  });

  addCard(slide, {
    x: 9.82,
    y: 4.54,
    w: 1.9,
    h: 1.1,
    fill: C.tealSoft,
    line: "98E1D7",
    kicker: "STANDARD",
    kickerFill: "D7F8F2",
    kickerColor: C.teal,
    kickerWidth: 0.95,
    title: "Tools",
    body: "click · type\nscroll · back\nabandon",
    titleColor: C.teal,
    bodyColor: "0E5A57",
  });

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 1.02,
    y: 6.12,
    w: 10.72,
    h: 0.52,
    rectRadius: 0.08,
    fill: { color: C.graySoft },
    line: { color: C.grayBorder, width: 1 },
  });
  addTag(slide, "MEMORY", {
    x: 1.18,
    y: 6.25,
    w: 0.92,
    h: 0.22,
    fill: "E2E8F0",
    line: "E2E8F0",
    color: C.muted,
    fontSize: 7.2,
  });
  slide.addText("단기: 현재 세션 행동 로그 · 감정 궤적   |   장기: 기억 스트림 · 반추 · 습관 강도 · 만족 추이", {
    x: 2.24,
    y: 6.28,
    w: 9.2,
    h: 0.14,
    fontFace: "Noto Sans CJK KR",
    fontSize: 8.1,
    color: C.ink,
    margin: 0,
  });

  addArrow(slide, {
    x1: 2.0,
    y1: 1.96,
    x2: 2.0,
    y2: 2.48,
    color: C.blue,
    lx: 2.13,
    ly: 1.9,
    lw: 1.05,
    label: "Observe",
    labelColor: C.blue,
    labelBold: true,
  });

  addArrow(slide, {
    x1: 3.22,
    y1: 4.18,
    x2: 3.58,
    y2: 3.38,
    color: C.orange,
  });

  addArrow(slide, {
    x1: 3.22,
    y1: 3.02,
    x2: 3.56,
    y2: 3.02,
    color: C.blue,
  });

  addArrow(slide, {
    x1: 6.42,
    y1: 4.52,
    x2: 6.42,
    y2: 4.0,
    color: C.orange,
    lx: 6.63,
    ly: 4.16,
    lw: 1.18,
    label: "감정·인지 상태 주입",
    labelColor: C.orange,
    labelSize: 7.1,
    labelBold: true,
    labelAlign: "left",
  });

  addArrow(slide, {
    x1: 7.04,
    y1: 3.04,
    x2: 7.42,
    y2: 3.04,
    color: C.line,
  });
  addArrow(slide, {
    x1: 9.54,
    y1: 3.1,
    x2: 10.26,
    y2: 4.54,
    color: C.teal,
  });

  addArrow(slide, {
    x1: 11.72,
    y1: 4.55,
    x2: 11.72,
    y2: 1.96,
    color: C.teal,
    lx: 11.1,
    ly: 2.05,
    lw: 1.1,
    label: "Act",
    labelColor: C.teal,
    labelBold: true,
  });

  addArrow(slide, {
    x1: 5.32,
    y1: 4.24,
    x2: 5.32,
    y2: 4.52,
    color: C.orange,
    dash: "dash",
    endArrow: true,
  });

  addFooterNote(
    slide,
    "핵심 차별점: 감정을 LLM이 즉흥적으로 정하는 대신, 외부 수학 엔진이 계산한 상태를 Brain에 주입합니다.",
    9.56,
    2.34,
    2.62
  );

  warnIfSlideHasOverlaps(slide, pptx);
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

function buildComparisonPanel(slide, x, y, w, h, cfg) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.12,
    fill: { color: cfg.panelFill },
    line: { color: cfg.panelLine, width: 1.2 },
  });

  addTag(slide, cfg.header, {
    x: x + 0.18,
    y: y + 0.18,
    w: 1.48,
    h: 0.26,
    fill: cfg.headerFill,
    line: cfg.headerFill,
    color: cfg.headerColor,
    fontSize: 7.4,
  });

  slide.addText(cfg.title, {
    x: x + 0.2,
    y: y + 0.44,
    w: w - 0.4,
    h: 0.24,
    fontFace: "NanumSquare",
    fontSize: 15.2,
    bold: true,
    color: C.ink,
    margin: 0,
  });

  cfg.cards.forEach((card) => {
    addCard(slide, card);
  });

  cfg.arrows.forEach((arrow) => addArrow(slide, arrow));
}

function buildCompareStat(slide, x, y, w, title, leftText, rightText, accentColor, accentFill) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h: 1.02,
    rectRadius: 0.08,
    fill: { color: "FFFFFF" },
    line: { color: C.grayBorder, width: 1 },
  });
  addTag(slide, title, {
    x: x + 0.12,
    y: y + 0.12,
    w: 0.88,
    h: 0.22,
    fill: accentFill,
    line: accentFill,
    color: accentColor,
    fontSize: 7.2,
  });
  slide.addText(`일반: ${leftText}`, {
    x: x + 0.14,
    y: y + 0.46,
    w: w - 0.28,
    h: 0.16,
    fontFace: "Noto Sans CJK KR",
    fontSize: 8.1,
    color: C.muted,
    margin: 0,
  });
  slide.addText(`Personica: ${rightText}`, {
    x: x + 0.14,
    y: y + 0.67,
    w: w - 0.28,
    h: 0.16,
    fontFace: "Noto Sans CJK KR",
    fontSize: 8.1,
    bold: true,
    color: accentColor,
    margin: 0,
  });
}

function buildComparisonSlide() {
  const slide = pptx.addSlide();
  addSlideBase(
    slide,
    "General AI Agent vs Personica Agent",
    "구조는 같지만, Personica는 Profile과 Emotion & Cognition Engine을 분리 모듈로 추가해 감정 계산과 페르소나 분화를 통제합니다."
  );

  buildComparisonPanel(slide, 0.7, 1.38, 5.82, 4.74, {
    panelFill: "F8FBFF",
    panelLine: "D6E4FF",
    header: "STANDARD AGENT",
    headerFill: C.blueSoft,
    headerColor: C.blue,
    title: "일반 AI Agent",
    cards: [
      {
        x: 1.84,
        y: 2.18,
        w: 3.36,
        h: 0.62,
        fill: C.blueSoft,
        line: C.blueBorder,
        shadow: false,
        title: "Perception",
        body: "",
        titleColor: C.blue,
        titleSize: 13,
        bodyH: 0,
        bodyY: 0.55,
        align: "center",
      },
      {
        x: 1.66,
        y: 3.02,
        w: 3.72,
        h: 1.04,
        fill: C.grayCard,
        line: C.grayBorder,
        title: "Brain (LLM)",
        body: "해석 · 판단 · 감정도 LLM이 직접 판단",
        titleSize: 14.2,
        bodyY: 0.5,
        bodyH: 0.34,
        bodySize: 8.1,
        align: "center",
      },
      {
        x: 1.84,
        y: 4.18,
        w: 3.36,
        h: 0.62,
        fill: C.blueSoft,
        line: C.blueBorder,
        shadow: false,
        title: "Planning",
        body: "",
        titleColor: C.blue,
        titleSize: 13,
        bodyH: 0,
        bodyY: 0.55,
        align: "center",
      },
      {
        x: 1.66,
        y: 4.94,
        w: 3.72,
        h: 0.54,
        fill: C.tealSoft,
        line: "98E1D7",
        shadow: false,
        title: "Tools → Action",
        body: "",
        titleColor: C.teal,
        titleSize: 13.2,
        bodyH: 0,
        bodyY: 0.55,
        align: "center",
      },
      {
        x: 1.66,
        y: 5.60,
        w: 3.72,
        h: 0.22,
        fill: C.graySoft,
        line: C.graySoft,
        shadow: false,
        title: "Memory",
        body: "",
        titleColor: C.ink,
        titleSize: 8.6,
        titleH: 0.12,
        bodyH: 0,
        bodyY: 0.15,
        align: "center",
      },
    ],
    arrows: [
      { x1: 3.52, y1: 2.8, x2: 3.52, y2: 3.0, color: C.line },
      { x1: 3.52, y1: 4.06, x2: 3.52, y2: 4.16, color: C.line },
      { x1: 3.52, y1: 4.8, x2: 3.52, y2: 4.92, color: C.line },
    ],
  });

  buildComparisonPanel(slide, 6.8, 1.38, 5.82, 4.74, {
    panelFill: "FFF9F5",
    panelLine: "F5C6A5",
    header: "PERSONICA AGENT",
    headerFill: C.orangeSoft,
    headerColor: C.orange,
    title: "Personica Agent",
    cards: [
      {
        x: 7.98,
        y: 2.14,
        w: 3.42,
        h: 0.5,
        fill: C.blueSoft,
        line: C.blueBorder,
        shadow: false,
        title: "Perception",
        body: "",
        titleColor: C.blue,
        titleSize: 12.6,
        bodyH: 0,
        bodyY: 0.4,
        align: "center",
      },
      {
        x: 7.8,
        y: 2.82,
        w: 3.78,
        h: 0.58,
        fill: C.orangeSoft,
        line: C.orangeBorder,
        shadow: false,
        title: "Profile (Big Five → 행동 파라미터)",
        body: "",
        titleColor: C.orange,
        titleSize: 11.6,
        bodyH: 0,
        bodyY: 0.5,
        align: "center",
      },
      {
        x: 7.84,
        y: 3.62,
        w: 3.7,
        h: 0.86,
        fill: C.grayCard,
        line: C.grayBorder,
        title: "Brain (LLM)",
        body: "해석 · 사고 + 외부 계산 감정 상태 주입",
        titleSize: 14.2,
        bodyY: 0.46,
        bodyH: 0.26,
        bodySize: 8,
        align: "center",
      },
      {
        x: 7.34,
        y: 4.72,
        w: 1.78,
        h: 0.72,
        fill: C.blueSoft,
        line: C.blueBorder,
        shadow: false,
        title: "Planning",
        body: "",
        titleColor: C.blue,
        titleSize: 11.8,
        bodyH: 0,
        bodyY: 0.6,
        align: "center",
      },
      {
        x: 9.42,
        y: 4.56,
        w: 2.36,
        h: 0.92,
        fill: C.orangeSoft,
        line: C.orangeBorder,
        shadow: false,
        title: "Emotion &\nCognition",
        body: "LLM 외부 수학 계산",
        titleColor: C.orange,
        titleSize: 11.8,
        bodyY: 0.62,
        bodyH: 0.2,
        bodySize: 7.6,
        align: "center",
      },
      {
        x: 7.82,
        y: 5.56,
        w: 3.76,
        h: 0.34,
        fill: C.tealSoft,
        line: "98E1D7",
        shadow: false,
        title: "Tools → Action",
        body: "",
        titleColor: C.teal,
        titleSize: 11.8,
        titleH: 0.14,
        bodyH: 0,
        bodyY: 0.45,
        align: "center",
      },
      {
        x: 7.82,
        y: 6.00,
        w: 3.76,
        h: 0.18,
        fill: C.graySoft,
        line: C.graySoft,
        shadow: false,
        title: "Memory",
        body: "",
        titleColor: C.ink,
        titleSize: 8.0,
        titleH: 0.1,
        bodyH: 0,
        bodyY: 0.15,
        align: "center",
      },
    ],
    arrows: [
      { x1: 9.69, y1: 2.64, x2: 9.69, y2: 2.8, color: C.orange },
      { x1: 9.69, y1: 3.4, x2: 9.69, y2: 3.6, color: C.line },
      { x1: 9.18, y1: 4.48, x2: 8.6, y2: 4.7, color: C.line },
      {
        x1: 10.6,
        y1: 4.56,
        x2: 10.1,
        y2: 4.28,
        color: C.orange,
      },
      { x1: 9.7, y1: 5.48, x2: 9.7, y2: 5.54, color: C.line },
      { x1: 9.7, y1: 5.9, x2: 9.7, y2: 5.98, color: C.line },
    ],
  });

  buildCompareStat(
    slide,
    0.82,
    6.32,
    3.92,
    "Emotion",
    "감정을 LLM이 직접 판단",
    "수학 계산 후 LLM에 주입",
    C.orange,
    C.orangeSoft
  );
  buildCompareStat(
    slide,
    4.98,
    6.32,
    3.34,
    "Bias",
    "긍정 편향이 그대로 노출",
    "구조적으로 완화",
    C.rose,
    C.roseSoft
  );
  buildCompareStat(
    slide,
    8.56,
    6.32,
    3.94,
    "Differentiation",
    "페르소나 분화가 약함",
    "페르소나별 다른 반응 보장",
    C.green,
    C.greenSoft
  );

  warnIfSlideHasOverlaps(slide, pptx);
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

async function main() {
  buildArchitectureSlide();
  buildComparisonSlide();
  await pptx.writeFile({ fileName: OUT_PATH });
  console.log(`Wrote ${OUT_PATH}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});



