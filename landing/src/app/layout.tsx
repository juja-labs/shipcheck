import type { Metadata } from "next";
import { Geist, Geist_Mono, Instrument_Serif } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const instrumentSerif = Instrument_Serif({
  weight: "400",
  variable: "--font-instrument-serif",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ShipCheck — 출시 전에, 20명이 써봤습니다",
  description:
    "AI 페르소나가 당신의 제품을 사람처럼 사용하고, 솔직하게 리뷰합니다. URL 하나로 5분이면 충분합니다.",
  openGraph: {
    title: "ShipCheck — 출시 전에, 20명이 써봤습니다",
    description:
      "AI 페르소나가 당신의 제품을 사람처럼 사용하고, 솔직하게 리뷰합니다.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${instrumentSerif.variable} font-sans antialiased bg-background text-foreground`}
      >
        {children}
      </body>
    </html>
  );
}
