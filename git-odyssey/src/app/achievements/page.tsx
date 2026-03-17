"use client";

import { useGameStore } from "@/store/gameStore";
import { Sidebar } from "@/components/layout/Sidebar";
import { Trophy, Star, Shield, Zap, Medal } from "lucide-react";
import { motion } from "framer-motion";

const ACHIEVEMENTS_DATA = [
  {
    id: "first_blood",
    title: "First Commit",
    description: "You successfully completed your first repository snapshot.",
    icon: <Star className="w-6 h-6" />,
    color: "from-yellow-400 to-yellow-600",
    reqMission: "phase-1-mission-1"
  },
  {
    id: "multiverse",
    title: "Multiverse Creator",
    description: "You branched out and created an alternate timeline.",
    icon: <Zap className="w-6 h-6" />,
    color: "from-brand-400 to-brand-600",
    reqMission: "phase-3-mission-1"
  },
  {
    id: "master_merger",
    title: "Master Merger",
    description: "You securely merged a branch without conflicts.",
    icon: <Shield className="w-6 h-6" />,
    color: "from-emerald-400 to-emerald-600",
    reqMission: "phase-3-mission-2" // Future mission
  },
  {
    id: "git_guru",
    title: "Git Guru",
    description: "Reached level 10 and mastered the Git internals.",
    icon: <Medal className="w-6 h-6" />,
    color: "from-purple-400 to-purple-600",
    reqMission: "level_10"
  }
];

export default function AchievementsPage() {
  const completedMissions = useGameStore(state => state.completedMissions);
  const xp = useGameStore(state => state.xp);
  const level = useGameStore(state => state.level);

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden relative selection:bg-brand-500/30">
      
      {/* Decorative Grid Background */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:64px_64px] pointer-events-none" />

      <Sidebar />

      <main className="flex-1 flex flex-col min-w-0 z-10 overflow-y-auto custom-scrollbar">
        {/* Top Header */}
        <header className="h-16 border-b border-white/5 bg-surface-dark/30 flex items-center px-6 backdrop-blur-md justify-between sticky top-0 z-20">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Trophy className="w-5 h-5 text-yellow-500" />
              Your Achievements
            </h2>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium text-neutral-400">
             Level: <span className="text-white bg-white/10 px-2 py-1 rounded">{level}</span>
             XP: <span className="text-brand-400">{xp}</span>
          </div>
        </header>

        <div className="max-w-5xl mx-auto w-full p-8 md:p-12">
          
          <div className="mb-12">
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight mb-4 text-white">
              Trophy Room
            </h1>
            <p className="text-neutral-400 text-lg">
              Track your milestones as you progress from a Git novice to a master of the command line. Complete missions and level up to unlock more badges.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {ACHIEVEMENTS_DATA.map((achievement, i) => {
              // Determine if achievement is unlocked
              const isUnlocked = 
                (achievement.reqMission.startsWith('phase') && completedMissions.includes(achievement.reqMission)) ||
                (achievement.reqMission === 'level_10' && level >= 10);
              
              return (
                <motion.div
                  key={achievement.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className={`relative overflow-hidden rounded-2xl border p-6 ${isUnlocked ? 'bg-surface-dark border-white/10 shadow-xl' : 'bg-surface-dark/40 border-white/5 opacity-60 grayscale'}`}
                >
                  <div className="relative z-10">
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 text-white bg-gradient-to-tr ${isUnlocked ? achievement.color : 'from-neutral-700 to-neutral-600'}`}>
                      {achievement.icon}
                    </div>
                    
                    <h3 className="text-xl font-bold text-white mb-2">
                      {achievement.title}
                    </h3>
                    
                    <p className="text-sm text-neutral-400">
                      {isUnlocked ? achievement.description : 'Keep learning to unlock this achievement.'}
                    </p>
                  </div>

                  {/* Shines and glow effects for unlocked ones */}
                  {isUnlocked && (
                    <div className={`absolute -bottom-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-20 bg-gradient-to-tr ${achievement.color} pointer-events-none`} />
                  )}
                  
                  {isUnlocked && (
                    <div className="absolute top-4 right-4 bg-white/10 text-white text-[10px] uppercase tracking-wider font-bold px-2 py-1 rounded border border-white/10">
                      Unlocked
                    </div>
                  )}
                  {!isUnlocked && (
                    <div className="absolute top-4 right-4 bg-black/20 text-neutral-500 text-[10px] uppercase tracking-wider font-bold px-2 py-1 rounded border border-white/5">
                      Locked
                    </div>
                  )}
                </motion.div>
              );
            })}
          </div>

        </div>
      </main>
    </div>
  );
}
