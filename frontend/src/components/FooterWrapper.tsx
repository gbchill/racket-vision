'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';

export default function FooterWrapper() {
  const pathname = usePathname();
  const hideFooterPaths = ['/upload'];
  
  // Don't render footer on specified paths
  if (hideFooterPaths.includes(pathname)) {
    return null;
  }

  // Return the footer component content directly
  return (
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
                <li><Link href="/features" className="hover:text-green-400 transition-colors">Features</Link></li>
                <li><Link href="/pricing" className="hover:text-green-400 transition-colors">Pricing</Link></li>
                <li><Link href="/showcase" className="hover:text-green-400 transition-colors">Showcase</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-medium mb-3">Resources</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/blog" className="hover:text-green-400 transition-colors">Blog</Link></li>
                <li><Link href="/guides" className="hover:text-green-400 transition-colors">Guides</Link></li>
                <li><Link href="/faq" className="hover:text-green-400 transition-colors">FAQ</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-medium mb-3">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/about" className="hover:text-green-400 transition-colors">About</Link></li>
                <li><Link href="/contact" className="hover:text-green-400 transition-colors">Contact</Link></li>
                <li><Link href="/careers" className="hover:text-green-400 transition-colors">Careers</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-medium mb-3">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/privacy" className="hover:text-green-400 transition-colors">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-green-400 transition-colors">Terms</Link></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-800 text-sm">
          <p>&copy; {new Date().getFullYear()} RacketVision. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}