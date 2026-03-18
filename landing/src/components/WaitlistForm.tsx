"use client";

import { useState, type FormEvent } from "react";

export function WaitlistForm({
  variant = "hero",
}: {
  variant?: "hero" | "bottom";
}) {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!email) return;
    setStatus("loading");
    // TODO: POST to /api/waitlist or external service (Mailchimp, Resend, etc.)
    await new Promise((resolve) => setTimeout(resolve, 900));
    setStatus("success");
  }

  if (status === "success") {
    return (
      <div
        className={`flex items-center gap-2.5 ${variant === "hero" ? "text-lg" : "text-base"} text-mint font-medium`}
      >
        <svg
          className="w-5 h-5 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2.5}
            d="M5 13l4 4L19 7"
          />
        </svg>
        등록 완료! 출시되면 가장 먼저 알려드릴게요.
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className={`flex ${variant === "hero" ? "flex-col sm:flex-row" : "flex-col sm:flex-row justify-center"} gap-3 w-full ${variant === "bottom" ? "max-w-md mx-auto" : "max-w-lg"}`}
    >
      <input
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        className="flex-1 px-4 py-3 rounded-lg bg-surface border border-edge text-foreground placeholder:text-faded focus:outline-none focus:border-mint focus:ring-1 focus:ring-mint/30 transition-colors"
      />
      <button
        type="submit"
        disabled={status === "loading"}
        className="px-6 py-3 rounded-lg bg-mint text-background font-semibold hover:bg-mint-bright active:scale-[0.98] transition-all disabled:opacity-50 whitespace-nowrap cursor-pointer"
      >
        {status === "loading" ? "등록 중..." : "무료 체험 신청"}
      </button>
    </form>
  );
}
