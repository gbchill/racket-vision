import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

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
        <main>{children}</main>
        <footer className="bg-black text-gray-400 py-8 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between">
              <div className="mb-6 md:mb-0">
                <h3 className="text-white text-lg font-semibold mb-2">RacketVision</h3>
                <p className="text-sm">AI-powered tennis coaching platform</p>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div>
                  <h4 className="text-white font-medium mb-3">Product</h4>
                  <ul className="space-y-2 text-sm">
                    <li><a href="/features" className="hover:text-green-400 transition-colors">Features</a></li>
                    <li><a href="/pricing" className="hover:text-green-400 transition-colors">Pricing</a></li>
                    <li><a href="/showcase" className="hover:text-green-400 transition-colors">Showcase</a></li>
                  </ul>
                </div>
                <div>
                  <h4 className="text-white font-medium mb-3">Resources</h4>
                  <ul className="space-y-2 text-sm">
                    <li><a href="/blog" className="hover:text-green-400 transition-colors">Blog</a></li>
                    <li><a href="/guides" className="hover:text-green-400 transition-colors">Guides</a></li>
                    <li><a href="/faq" className="hover:text-green-400 transition-colors">FAQ</a></li>
                  </ul>
                </div>
                <div>
                  <h4 className="text-white font-medium mb-3">Company</h4>
                  <ul className="space-y-2 text-sm">
                    <li><a href="/about" className="hover:text-green-400 transition-colors">About</a></li>
                    <li><a href="/contact" className="hover:text-green-400 transition-colors">Contact</a></li>
                    <li><a href="/careers" className="hover:text-green-400 transition-colors">Careers</a></li>
                  </ul>
                </div>
                <div>
                  <h4 className="text-white font-medium mb-3">Legal</h4>
                  <ul className="space-y-2 text-sm">
                    <li><a href="/privacy" className="hover:text-green-400 transition-colors">Privacy</a></li>
                    <li><a href="/terms" className="hover:text-green-400 transition-colors">Terms</a></li>
                  </ul>
                </div>
              </div>
            </div>
            <div className="mt-8 pt-8 border-t border-gray-800 text-sm">
              <p>&copy; {new Date().getFullYear()} RacketVision. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}