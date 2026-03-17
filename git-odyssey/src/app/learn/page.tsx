import { Sidebar } from "@/components/layout/Sidebar";
import SimulatedTerminal from "@/components/terminal/SimulatedTerminal";
import { GitGraph } from "@/components/visualizer/GitGraph";
import { MissionPanel } from "@/components/lesson/MissionPanel";

export default function LearnWorkspace() {
  return (
    <div className="flex h-screen w-full bg-background overflow-hidden relative selection:bg-brand-500/30">
      
      {/* Decorative Grid Background - Adding here to ensure no pointer block */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:64px_64px] pointer-events-none" />

      <Sidebar />

      <main className="flex-1 flex flex-col min-w-0 z-10">
        {/* Top Header */}
        <header className="h-16 border-b border-white/5 bg-surface-dark/30 flex items-center px-6 backdrop-blur-md justify-between">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold text-white">Learning Workspace</h2>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium text-neutral-400">
             XP: <span className="text-brand-400">100</span>
          </div>
        </header>

        {/* Workspace Layout */}
        <div className="flex-1 flex flex-col lg:flex-row overflow-hidden p-4 gap-4">
          
          {/* Mission & Visualizer Panel */}
          <div className="flex-1 flex flex-col gap-4 min-h-0 relative overflow-hidden">
            
            <MissionPanel />

            {/* Git Graph Visualizer */}
            <div className="flex-1 bg-surface-dark border border-white/5 rounded-2xl shadow-xl overflow-hidden flex flex-col relative min-h-[300px]">
               <div className="px-4 py-3 border-b border-white/5 bg-white/5 flex items-center justify-between">
                 <span className="text-xs font-semibold text-neutral-400 uppercase tracking-wider">Repository Graph</span>
                 <div className="flex gap-2">
                   <button className="text-xs bg-white/5 hover:bg-white/10 px-2 py-1 rounded text-neutral-300 transition">Objects</button>
                   <button className="text-xs bg-white/10 px-2 py-1 rounded text-white transition font-medium border border-white/10 shadow shadow-black/50">Graph</button>
                 </div>
               </div>
               <GitGraph />
            </div>

          </div>

          {/* Terminal Panel */}
          <div className="w-full lg:w-[45%] flex-shrink-0 h-[400px] lg:h-auto z-10">
            <SimulatedTerminal />
          </div>

        </div>
      </main>

    </div>
  );
}
