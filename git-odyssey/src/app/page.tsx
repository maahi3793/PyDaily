import Link from "next/link";
import { Terminal, GitBranch, ArrowRight, BookOpen } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-background-dark via-surface-dark to-background-dark text-white relative overflow-hidden">
      
      {/* Decorative Grid Background */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:64px_64px] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none" />

      {/* Header */}
      <header className="px-6 py-8 flex items-center justify-between z-10">
        <div className="flex items-center gap-2 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-500 flex items-center justify-center shadow-lg group-hover:shadow-brand-500/50 transition-all duration-300">
            <GitBranch className="text-white w-6 h-6" />
          </div>
          <span className="font-bold text-2xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-neutral-400">
            Git Odyssey
          </span>
        </div>
        <nav>
           <Link 
            href="/learn" 
            className="px-5 py-2.5 rounded-full bg-white/10 hover:bg-white/15 border border-white/10 backdrop-blur-md transition-all font-medium text-sm flex items-center gap-2"
          >
            Go to Platform <ArrowRight className="w-4 h-4" />
          </Link>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center -mt-20 px-6 z-10">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-500 text-sm font-medium mb-4">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500"></span>
            </span>
            Interactive Learning Experience v1.0
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight">
            Master Git from <br className="hidden md:block"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-cyan-400">
              zero to expert
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-neutral-400 max-w-2xl mx-auto font-light leading-relaxed">
            A premium, gamified learning platform with a simulated terminal, live visual graph, and interactive missions. Stop guessing and start understanding.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-6">
            <Link 
              href="/learn"
              className="w-full sm:w-auto px-8 py-4 rounded-full bg-brand-600 hover:bg-brand-500 text-white font-semibold flex items-center justify-center gap-2 transition-all shadow-[0_0_40px_-10px_rgba(59,130,246,0.5)] hover:shadow-[0_0_60px_-15px_rgba(59,130,246,0.6)] transform hover:-translate-y-1"
            >
              <Terminal className="w-5 h-5" />
              Start Your Journey
            </Link>
            <Link 
              href="/curriculum"
              className="w-full sm:w-auto px-8 py-4 rounded-full bg-surface-dark/50 hover:bg-surface-dark border border-white/10 text-neutral-200 font-semibold flex items-center justify-center gap-2 transition-all backdrop-blur-sm"
            >
              <BookOpen className="w-5 h-5" />
              View Curriculum
            </Link>
          </div>
        </div>

        {/* Feature Preview Mockup */}
        <div className="mt-20 w-full max-w-5xl rounded-2xl border border-white/10 bg-black/40 backdrop-blur-xl p-2 shadow-2xl relative">
          <div className="absolute inset-0 bg-gradient-to-t from-background-dark via-transparent to-transparent pointer-events-none rounded-2xl" />
          <div className="h-64 sm:h-96 w-full rounded-xl border border-white/5 bg-[#0d0d0f] flex items-center justify-center overflow-hidden relative">
            {/* Fake UI */}
            <div className="absolute inset-x-0 top-0 h-10 border-b border-white/5 bg-white/5 flex items-center px-4 gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500/80" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
              <div className="w-3 h-3 rounded-full bg-green-500/80" />
            </div>
            <div className="font-mono text-sm text-neutral-500 opacity-50 flex items-center gap-2">
              <Terminal className="w-4 h-4" /> root@git-odyssey ~ $ git init
            </div>
          </div>
        </div>
      </main>

    </div>
  );
}
