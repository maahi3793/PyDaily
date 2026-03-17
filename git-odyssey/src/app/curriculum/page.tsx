import Link from "next/link";
import { ArrowLeft, BookOpen, CheckCircle2, GitBranch, Terminal } from "lucide-react";
import { ALL_MISSIONS } from "@/lib/curriculum/phases";

export default function CurriculumPage() {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-background-dark via-surface-dark to-background-dark text-white relative overflow-hidden selection:bg-brand-500/30">
      
      {/* Decorative Grid Background */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:64px_64px] pointer-events-none" />

      {/* Header */}
      <header className="px-6 py-6 border-b border-white/5 bg-surface-dark/50 backdrop-blur-md sticky top-0 z-20 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/" className="p-2 rounded-full hover:bg-white/10 transition">
            <ArrowLeft className="w-5 h-5 text-neutral-400" />
          </Link>
          <div className="flex items-center gap-2 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-brand-600 to-brand-500 flex items-center justify-center shadow-lg">
              <BookOpen className="text-white w-4 h-4" />
            </div>
            <span className="font-bold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-neutral-400">
              Curriculum
            </span>
          </div>
        </div>
        <Link 
          href="/learn" 
          className="px-4 py-2 rounded-full bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm flex items-center gap-2 transition shadow-[0_0_20px_-5px_rgba(59,130,246,0.5)]"
        >
          <Terminal className="w-4 h-4" />
          Jump to Workspace
        </Link>
      </header>

      {/* Main Content */}
      <main className="flex-1 w-full max-w-4xl mx-auto p-6 md:p-12 z-10">
        
        <div className="mb-12">
          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight mb-4">
            The Learning Journey
          </h1>
          <p className="text-neutral-400 text-lg">
            Master Git sequentially. Build your knowledge from basic snapshotting all the way to complex multi-branch merges and internal object management.
          </p>
        </div>

        {/* Phase List */}
        <div className="space-y-8 relative before:absolute before:inset-y-0 before:left-[19px] before:w-0.5 before:bg-white/10">
          
          {ALL_MISSIONS.map((mission, index) => (
            <div key={mission.id} className="relative flex items-start gap-8 group">
              
              {/* Timeline Marker */}
              <div className="mt-1.5 w-10 h-10 rounded-full border-[4px] border-[#0d0d0f] bg-surface-dark ring-2 ring-white/10 flex items-center justify-center shrink-0 z-10 group-hover:ring-brand-500/50 transition-all">
                <span className="text-sm font-bold text-neutral-400 group-hover:text-brand-400">
                  {index + 1}
                </span>
              </div>
              
              {/* Mission Card */}
              <div className="bg-surface-dark/80 border border-white/5 p-6 md:p-8 rounded-2xl shadow-xl flex-1 backdrop-blur-md group-hover:border-brand-500/20 transition-colors">
                
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
                  <div>
                    <h2 className="text-xl md:text-2xl font-bold text-white mb-2">
                      {mission.title}
                    </h2>
                    <p className="text-neutral-400 text-sm md:text-base leading-relaxed">
                      {mission.story}
                    </p>
                  </div>
                  <div className="flex shrink-0 items-center justify-center px-4 py-2 rounded-lg bg-git-commit/10 border border-git-commit/20 text-git-commit font-bold text-sm">
                    +{mission.xpReward} XP
                  </div>
                </div>

                <div className="mt-6 border-t border-white/5 pt-6">
                  <h4 className="text-xs uppercase tracking-wider font-semibold text-neutral-500 mb-4 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4" /> Learning Objectives
                  </h4>
                  <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {mission.objectives.map((obj) => (
                      <li key={obj.id} className="flex items-start gap-2 text-sm text-neutral-300">
                        <div className="mt-1 w-1.5 h-1.5 rounded-full bg-brand-500/50 shrink-0" />
                        {obj.description}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="mt-6 flex justify-end">
                  <Link 
                    href="/learn"
                    className="flex items-center gap-2 text-sm font-medium text-brand-400 hover:text-brand-300 transition"
                  >
                    Start Mission <ArrowLeft className="w-4 h-4 rotate-180" />
                  </Link>
                </div>
              </div>

            </div>
          ))}

          {/* Phase: Coming Soon */}
          <div className="relative flex items-start gap-8 opacity-50 grayscale pl-2">
             <div className="mt-1.5 w-6 h-6 rounded-full border-[4px] border-[#0d0d0f] bg-surface-dark shrink-0 z-10" />
             <div className="flex-1 py-1">
               <h3 className="text-lg font-semibold italic text-neutral-500">More phases unlocking soon...</h3>
             </div>
          </div>

        </div>

      </main>

    </div>
  );
}
