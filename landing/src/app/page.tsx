import { WaitlistForm } from "../components/WaitlistForm";
import { AnimateOnScroll } from "../components/AnimateOnScroll";

/* ── Data ──────────────────────────────────────────────── */

const problems = [
  {
    emoji: "👥",
    title: "지인에게 부탁",
    desc: '"좋은데?" 이상 안 나오는 편향된 3~5명의 피드백',
    result: "결과: 가짜 확신",
  },
  {
    emoji: "📣",
    title: "베타테스터 모집",
    desc: "2주 모집, 5명 지원, 실제 피드백은 1~2명",
    result: "결과: 시간 낭비",
  },
  {
    emoji: "💸",
    title: "UserTesting",
    desc: "$49/세션 × 5명 = $245+, 스크립트 작성은 덤",
    result: "결과: 예산 초과",
  },
  {
    emoji: "🚀",
    title: "그냥 출시",
    desc: "반응 없음. 원인 불명. 뭘 고쳐야 하는지도 모름",
    result: "결과: 원인불명 실패",
  },
];

const steps = [
  {
    num: "01",
    title: "URL 입력",
    desc: "제품 URL과 타겟 사용자를 알려주세요. 그게 전부입니다.",
  },
  {
    num: "02",
    title: "20명이 사용합니다",
    desc: "AI 페르소나가 실제로 클릭하고, 탐색하고, 막히고, 이탈합니다.",
  },
  {
    num: "03",
    title: "5분 후 리포트",
    desc: "세그먼트별 인사이트와 1인칭 사용기를 받아보세요.",
  },
];

const features = [
  {
    icon: "🎭",
    title: "다양한 페르소나",
    desc: "60대 은퇴 교사부터 Z세대 개발자까지. 나이, 기술 수준, 인내심, 가격 민감도가 모두 다른 20명.",
  },
  {
    icon: "🖱️",
    title: "실제 제품 사용",
    desc: "설문이나 인터뷰가 아닙니다. 실제 제품을 클릭하고 탐색하며, 사람처럼 행동합니다.",
  },
  {
    icon: "🧠",
    title: "감정 · 인지 시뮬레이션",
    desc: '인지 부하, 좌절감, 만족도를 실시간 추적. "왜 이탈했는가"를 인과적으로 설명합니다.',
  },
  {
    icon: "💬",
    title: "페르소나 인터뷰룸",
    desc: '리포트가 부족하면? 궁금한 페르소나에게 직접 "왜 거기서 멈췄어요?"라고 물어보세요.',
  },
];

const personas = [
  {
    initial: "서",
    name: "김서연",
    age: 28,
    role: "UX 디자이너",
    avatarBg: "bg-mint/20",
    avatarText: "text-mint",
    emotions: ["호기심", "만족", "혼란"],
    review:
      "온보딩은 깔끔했어요. 근데 대시보드 들어가니까 뭘 먼저 해야 할지 10초쯤 멍했어요. 왼쪽 사이드바에 메뉴가 7개인데 아이콘만 있고 텍스트가 없어서 하나하나 눌러봐야 했거든요.",
    tags: [
      { label: "인지 부하 높음", classes: "text-gold bg-gold/10" },
      { label: "이탈 위험", classes: "text-coral bg-coral/10" },
    ],
    insight: "대시보드 초기 가이드 필요 — 사용자 67%가 같은 지점에서 멈춤",
  },
  {
    initial: "영",
    name: "박영수",
    age: 62,
    role: "은퇴 교사",
    avatarBg: "bg-lavender/20",
    avatarText: "text-lavender",
    emotions: ["기대", "좌절", "이탈"],
    review:
      "글씨가 너무 작아서 확대를 했는데 레이아웃이 깨졌어요. 회원가입 할 때 비밀번호 조건이 영어로만 나와서 뭘 고쳐야 하는지 몰랐습니다. 3번 틀리고 나서 포기했어요.",
    tags: [
      { label: "접근성 문제", classes: "text-coral bg-coral/10" },
      { label: "완전 이탈", classes: "text-coral bg-coral/10" },
    ],
    insight:
      "시니어 사용자 전원 회원가입 이탈 — 비밀번호 에러 메시지 한국어화 필수",
  },
  {
    initial: "A",
    name: "Alex Chen",
    age: 34,
    role: "풀스택 개발자",
    avatarBg: "bg-mint/20",
    avatarText: "text-mint",
    emotions: ["중립", "긍정", "흥미"],
    review:
      "API 문서가 바로 보여서 좋았어요. 다크모드 지원도 깔끔하고. 근데 에러 메시지가 'Something went wrong'만 나오는 건 좀... 에러 코드라도 같이 보여주면 디버깅이 편할 텐데.",
    tags: [
      { label: "만족", classes: "text-mint bg-mint/10" },
      { label: "개선 제안", classes: "text-gold bg-gold/10" },
    ],
    insight: "개발자 세그먼트는 DX에 민감 — 에러 핸들링이 신뢰에 직결",
  },
];

const comparisonRows = [
  ["소요 시간", "5분", "1~2일", "2~3주", "1~2일"],
  ["비용", "$29~", "$245+", "무료", "무료"],
  ["페르소나 수", "20명+", "5명", "불확실", "3~5명"],
  ["다양성", "✓", "△", "△", "✗"],
  ["솔직도", "✓", "○", "○", "✗"],
  ["감정 분석", "✓", "✗", "✗", "✗"],
  ["즉시 반복", "✓", "✗", "✗", "✗"],
];

/* ── Page ──────────────────────────────────────────────── */

export default function Home() {
  return (
    <main className="min-h-screen overflow-x-hidden">
      {/* ─── Nav ─── */}
      <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-background/70 border-b border-edge/40">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <span className="font-serif text-xl italic text-foreground tracking-tight">
            ShipCheck
          </span>
          <a
            href="#waitlist"
            className="text-sm px-4 py-2 rounded-lg bg-mint/10 text-mint hover:bg-mint/20 transition-colors font-medium"
          >
            무료 체험 신청
          </a>
        </div>
      </nav>

      {/* ─── Hero ─── */}
      <section className="relative min-h-screen flex items-center pt-16">
        {/* Ambient gradients */}
        <div className="absolute top-1/4 -left-40 w-[600px] h-[600px] bg-mint/[0.07] rounded-full blur-[160px] pointer-events-none" />
        <div className="absolute bottom-1/4 -right-40 w-[500px] h-[500px] bg-lavender/[0.06] rounded-full blur-[160px] pointer-events-none" />

        <div className="max-w-6xl mx-auto px-6 grid lg:grid-cols-2 gap-12 lg:gap-20 items-center relative z-10">
          {/* Left — copy */}
          <div className="animate-fade-in-up">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-mint/10 text-mint text-sm font-medium mb-8">
              <span className="w-1.5 h-1.5 rounded-full bg-mint animate-pulse-glow" />
              AI 페르소나 시뮬레이션
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-[3.5rem] font-bold leading-[1.15] mb-6 tracking-tight">
              출시 전에,
              <br />
              <span className="text-mint">20명</span>이 써봤습니다.
            </h1>

            <p className="text-lg text-muted max-w-lg mb-8 leading-relaxed">
              60대 어르신부터 Z세대 개발자까지 — AI 페르소나가 당신의 제품을
              사람처럼 사용하고, 솔직하게 리뷰합니다.
              <br />
              <span className="text-foreground font-medium">
                URL 하나로 5분이면 충분합니다.
              </span>
            </p>

            <WaitlistForm variant="hero" />

            <p className="mt-4 text-sm text-faded">
              무료 1회 체험 · 카드 등록 불필요
            </p>
          </div>

          {/* Right — floating report card (desktop) */}
          <div className="hidden lg:flex justify-center">
            <div className="animate-float relative">
              <div className="bg-card border border-edge rounded-xl p-6 shadow-2xl shadow-mint/5 max-w-sm">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-mint/20 flex items-center justify-center text-mint font-semibold text-sm">
                    서
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground">
                      김서연, 28세
                    </p>
                    <p className="text-xs text-faded">UX 디자이너</p>
                  </div>
                  <div className="flex gap-1">
                    {["호기심", "만족", "혼란"].map((e) => (
                      <span
                        key={e}
                        className="text-[10px] px-1.5 py-0.5 rounded bg-surface text-muted"
                      >
                        {e}
                      </span>
                    ))}
                  </div>
                </div>
                <p className="text-sm text-muted italic leading-relaxed mb-4">
                  &ldquo;온보딩은 깔끔했어요. 근데 대시보드 들어가니까 뭘 먼저
                  해야 할지 10초쯤 멍했어요&hellip;&rdquo;
                </p>
                <div className="flex gap-2">
                  <span className="text-xs px-2 py-1 rounded-full text-gold bg-gold/10">
                    인지 부하 높음
                  </span>
                  <span className="text-xs px-2 py-1 rounded-full text-coral bg-coral/10">
                    이탈 위험
                  </span>
                </div>
              </div>
              {/* Stacked shadow cards */}
              <div className="absolute -bottom-3 -right-3 -z-10 bg-card/40 border border-edge/30 rounded-xl w-full h-full" />
              <div className="absolute -bottom-6 -right-6 -z-20 bg-card/20 border border-edge/20 rounded-xl w-full h-full" />
            </div>
          </div>
        </div>
      </section>

      {/* ─── Problem ─── */}
      <section className="py-24 lg:py-32 bg-surface/60">
        <div className="max-w-6xl mx-auto px-6">
          <AnimateOnScroll className="text-center mb-16">
            <p className="text-mint font-mono text-sm tracking-wider uppercase mb-3">
              The Problem
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              지금, 어떻게 검증하고 계세요?
            </h2>
            <p className="text-muted text-lg">대부분의 빌더가 겪는 현실</p>
          </AnimateOnScroll>

          <div className="grid sm:grid-cols-2 gap-5">
            {problems.map((p, i) => (
              <AnimateOnScroll key={p.title} delay={i * 100}>
                <div className="bg-card/80 border border-edge rounded-xl p-6 hover:border-edge/80 hover:bg-card transition-all h-full">
                  <div className="text-2xl mb-3">{p.emoji}</div>
                  <h3 className="text-lg font-semibold mb-2">{p.title}</h3>
                  <p className="text-muted text-sm leading-relaxed mb-4">
                    {p.desc}
                  </p>
                  <p className="text-sm font-mono text-coral/80">{p.result}</p>
                </div>
              </AnimateOnScroll>
            ))}
          </div>
        </div>
      </section>

      {/* ─── How It Works ─── */}
      <section className="py-24 lg:py-32">
        <div className="max-w-6xl mx-auto px-6">
          <AnimateOnScroll className="text-center mb-16">
            <p className="text-mint font-mono text-sm tracking-wider uppercase mb-3">
              How It Works
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              URL 하나면 됩니다
            </h2>
            <p className="text-muted text-lg">
              복잡한 설정이나 스크립트 없이, 3단계로 끝
            </p>
          </AnimateOnScroll>

          <div className="grid md:grid-cols-3 gap-10">
            {steps.map((s, i) => (
              <AnimateOnScroll key={s.num} delay={i * 150}>
                <div className="relative">
                  <span className="text-7xl font-bold text-mint/[0.08] font-mono absolute -top-10 -left-2 select-none">
                    {s.num}
                  </span>
                  <div className="pt-8 relative">
                    <h3 className="text-xl font-semibold mb-3">{s.title}</h3>
                    <p className="text-muted leading-relaxed">{s.desc}</p>
                  </div>
                  {i < steps.length - 1 && (
                    <div className="hidden md:block absolute top-14 -right-5 text-edge/60 text-xl">
                      &rarr;
                    </div>
                  )}
                </div>
              </AnimateOnScroll>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Features ─── */}
      <section className="py-24 lg:py-32 bg-surface/60">
        <div className="max-w-6xl mx-auto px-6">
          <AnimateOnScroll className="text-center mb-16">
            <p className="text-mint font-mono text-sm tracking-wider uppercase mb-3">
              Core Features
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              QA가 아닙니다
            </h2>
            <p className="text-muted text-lg">
              사람의 경험을 시뮬레이션합니다
            </p>
          </AnimateOnScroll>

          <div className="grid sm:grid-cols-2 gap-5">
            {features.map((f, i) => (
              <AnimateOnScroll key={f.title} delay={i * 100}>
                <div className="bg-card/80 border border-edge rounded-xl p-6 hover:border-mint/20 transition-all h-full">
                  <div className="text-2xl mb-3">{f.icon}</div>
                  <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
                  <p className="text-muted text-sm leading-relaxed">{f.desc}</p>
                </div>
              </AnimateOnScroll>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Sample Report ─── */}
      <section className="py-24 lg:py-32">
        <div className="max-w-6xl mx-auto px-6">
          <AnimateOnScroll className="text-center mb-16">
            <p className="text-mint font-mono text-sm tracking-wider uppercase mb-3">
              Sample Report
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              실제 리포트 미리보기
            </h2>
            <p className="text-muted text-lg">
              이런 수준의 피드백을 받게 됩니다
            </p>
          </AnimateOnScroll>

          <div className="grid lg:grid-cols-3 gap-6">
            {personas.map((p, i) => (
              <AnimateOnScroll key={p.name} delay={i * 150}>
                <div className="bg-card border border-edge rounded-xl p-6 hover:shadow-lg hover:shadow-mint/[0.04] transition-all h-full flex flex-col">
                  {/* Header */}
                  <div className="flex items-center gap-3 mb-3">
                    <div
                      className={`w-10 h-10 rounded-full ${p.avatarBg} flex items-center justify-center ${p.avatarText} font-semibold text-sm shrink-0`}
                    >
                      {p.initial}
                    </div>
                    <div>
                      <p className="text-sm font-medium">
                        {p.name}, {p.age}세
                      </p>
                      <p className="text-xs text-faded">{p.role}</p>
                    </div>
                  </div>

                  {/* Emotion flow */}
                  <div className="flex items-center gap-1 mb-4 flex-wrap">
                    {p.emotions.map((e, j) => (
                      <span key={e} className="flex items-center">
                        <span className="text-[11px] px-1.5 py-0.5 rounded bg-surface text-muted">
                          {e}
                        </span>
                        {j < p.emotions.length - 1 && (
                          <span className="text-faded text-xs mx-1">
                            &rarr;
                          </span>
                        )}
                      </span>
                    ))}
                  </div>

                  {/* Review */}
                  <blockquote className="text-sm text-muted italic leading-relaxed mb-4 border-l-2 border-edge pl-3 flex-1">
                    &ldquo;{p.review}&rdquo;
                  </blockquote>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {p.tags.map((t) => (
                      <span
                        key={t.label}
                        className={`text-xs px-2 py-1 rounded-full ${t.classes}`}
                      >
                        {t.label}
                      </span>
                    ))}
                  </div>

                  {/* Insight */}
                  <div className="bg-surface rounded-lg p-3 mt-auto">
                    <p className="text-xs text-muted leading-relaxed">
                      <span className="text-mint font-medium">
                        핵심 인사이트:
                      </span>{" "}
                      {p.insight}
                    </p>
                  </div>
                </div>
              </AnimateOnScroll>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Comparison ─── */}
      <section className="py-24 lg:py-32 bg-surface/60">
        <div className="max-w-5xl mx-auto px-6">
          <AnimateOnScroll className="text-center mb-16">
            <p className="text-mint font-mono text-sm tracking-wider uppercase mb-3">
              Comparison
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              비교해보세요
            </h2>
          </AnimateOnScroll>

          <AnimateOnScroll>
            <div className="overflow-x-auto -mx-6 px-6">
              <table className="w-full text-sm min-w-[540px]">
                <thead>
                  <tr className="border-b border-edge">
                    <th className="text-left py-4 px-4 text-faded font-medium w-28" />
                    <th className="py-4 px-4 text-mint font-semibold">
                      ShipCheck
                    </th>
                    <th className="py-4 px-4 text-muted font-medium">
                      UserTesting
                    </th>
                    <th className="py-4 px-4 text-muted font-medium">
                      베타 테스터
                    </th>
                    <th className="py-4 px-4 text-muted font-medium">
                      지인 피드백
                    </th>
                  </tr>
                </thead>
                <tbody className="text-center">
                  {comparisonRows.map(([label, ...values]) => (
                    <tr
                      key={label}
                      className="border-b border-edge/40 hover:bg-card/40 transition-colors"
                    >
                      <td className="text-left py-3.5 px-4 text-muted font-medium">
                        {label}
                      </td>
                      {values.map((v, j) => (
                        <td
                          key={j}
                          className={`py-3.5 px-4 ${j === 0 ? "text-mint font-semibold" : "text-faded"}`}
                        >
                          {v}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </AnimateOnScroll>
        </div>
      </section>

      {/* ─── Final CTA ─── */}
      <section id="waitlist" className="py-24 lg:py-32 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-mint/[0.04] to-background pointer-events-none" />
        <div className="max-w-2xl mx-auto px-6 text-center relative z-10">
          <AnimateOnScroll>
            <h2 className="text-3xl sm:text-4xl font-bold mb-4 leading-snug">
              5분 후,
              <br />
              제품을 다시 보게 됩니다
            </h2>
            <p className="text-muted text-lg mb-10">
              지금 등록하면 출시 즉시 무료 1회 체험을 드립니다.
            </p>
            <WaitlistForm variant="bottom" />
            <p className="mt-4 text-sm text-faded">
              스팸 없음 · 언제든 해지 가능
            </p>
          </AnimateOnScroll>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="py-8 border-t border-edge/30">
        <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row justify-between items-center gap-4">
          <span className="font-serif italic text-faded text-sm">
            ShipCheck
          </span>
          <p className="text-xs text-faded">
            &copy; 2026 ShipCheck. Built for builders.
          </p>
        </div>
      </footer>
    </main>
  );
}
