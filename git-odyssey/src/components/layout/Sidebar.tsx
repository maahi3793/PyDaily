"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { GitBranch, Book, Trophy, Home, RotateCcw } from "lucide-react";
import { useGameStore } from "@/store/gameStore";
import { useGitStore } from "@/store/gitStore";

export function Sidebar() {
  const pathname = usePathname();
  const resetProgress = useGameStore(state => state.resetProgress);
  const resetRepository = useGitStore(state => state.resetRepository);

  const handleReset = () => {
    if (confirm("Are you sure you want to reset all your learning progress? This cannot be undone.")) {
      resetProgress();
      resetRepository();
      window.location.reload(); // Hard refresh to clear any lingering layout state
    }
  };

  const navItems = [
    { name: "Missions", href: "/learn", icon: Book },
    { name: "Achievements", href: "/achievements", icon: Trophy },
    { name: "Back Home", href: "/", icon: Home },
  ];

  return (
    <aside className="w-64 border-r border-border-dark bg-surface-dark/50 flex flex-col backdrop-blur-md z-20">
      <div className="p-6 border-b border-border-dark flex items-center justify-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-brand-500 flex items-center justify-center shadow-lg">
          <GitBranch className="text-white w-6 h-6" />
        </div>
        <span className="font-bold text-xl tracking-tight text-white">Git Odyssey</span>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const IconStyle = item.icon;
          return (
            <Link 
              key={item.href}
              href={item.href} 
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors font-medium ${
                isActive 
                  ? "bg-brand-500/10 text-brand-400 border border-brand-500/20" 
                  : "text-neutral-400 hover:text-white hover:bg-white/5 border border-transparent"
              }`}
            >
              <IconStyle className="w-5 h-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border-dark">
        <button 
          onClick={handleReset}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-400/80 hover:text-red-400 hover:bg-red-400/10 transition-colors font-medium text-sm"
        >
          <RotateCcw className="w-4 h-4" />
          Start Over
        </button>
      </div>

      <div className="p-4 pt-2 font-sans text-xs text-neutral-500 text-center">
        v1.0.0
      </div>
    </aside>
  );
}
