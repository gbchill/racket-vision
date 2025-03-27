import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "../components/Navbar";
import FooterWrapper from "../components/FooterWrapper";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "RacketVision | AI Tennis Shot Analysis",
  description: "Improve your tennis game with AI-powered shot analysis. Upload your video and get instant feedback on your technique.",
  keywords: "tennis, coaching, AI, shot analysis, forehand, technique improvement, tennis training",
  authors: [{ name: "RacketVision" }],
  openGraph: {
    title: "RacketVision | AI Tennis Shot Analysis",
    description: "Improve your tennis game with AI-powered shot analysis. Upload your video and get instant feedback on your technique.",
    url: "https://racketvision.com",
    siteName: "RacketVision",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "RacketVision - AI Tennis Shot Analysis",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "RacketVision | AI Tennis Shot Analysis",
    description: "Improve your tennis game with AI-powered shot analysis. Upload your video and get instant feedback on your technique.",
    images: ["/twitter-image.jpg"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar />
        {children}
        <FooterWrapper />
      </body>
    </html>
  );
}