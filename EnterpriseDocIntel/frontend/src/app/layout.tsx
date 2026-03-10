import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Sidebar from '@/components/Sidebar';
import TopNav from '@/components/TopNav';

// We use Inter for a clean, Apple-like enterprise aesthetic
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: 'Enterprise Document Intelligence',
  description: 'Hybrid RAG Platform powered by local embeddings and cloud reasoning.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} font-sans antialiased h-full`}>
      <body className="flex h-full bg-slate-50 text-slate-900 overflow-hidden">
        
        {/* Left Sidebar */}
        <Sidebar />

        {/* Main Application Area */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          <TopNav />
          
          {/* Dynamic Page Content */}
          <main className="flex-1 overflow-y-auto p-8">
            <div className="mx-auto max-w-6xl h-full">
              {children}
            </div>
          </main>
        </div>
        
      </body>
    </html>
  );
}
