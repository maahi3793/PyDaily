"use client";

import { useGameStore } from "@/store/gameStore";
import { useGitStore } from "@/store/gitStore";
import { getMissionById } from "@/lib/curriculum/phases";
import { checkObjective, isMissionComplete } from "@/lib/curriculum/validator";
import { CheckCircle2, Circle, ChevronRight, Check, BookOpen } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";
import confetti from "canvas-confetti";

export function MissionPanel() {
  const activeMissionId = useGameStore(state => state.activeMissionId);
  const addXp = useGameStore(state => state.addXp);
  const completeMission = useGameStore(state => state.completeMission);
  const completedMissions = useGameStore(state => state.completedMissions);
  
  const repoState = useGitStore(state => state.repoState);

  const [showSuccess, setShowSuccess] = useState(false);
  const [isReadingMode, setIsReadingMode] = useState(true);

  // Derive active mission data
  const mission = activeMissionId ? getMissionById(activeMissionId) : null;
  const isComplete = mission ? isMissionComplete(mission, repoState) : false;
  
  // Confetti trigger and check
  useEffect(() => {
    if (mission && isComplete && !completedMissions.includes(mission.id)) {
      completeMission(mission.id);
      addXp(mission.xpReward);
      
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#3b82f6', '#10b981', '#fbbf24']
      });
      
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 5000);
    }
  }, [isComplete, mission, completedMissions, completeMission, addXp]);

  // Reset reading mode when mission changes
  useEffect(() => {
    setIsReadingMode(true);
  }, [activeMissionId]);


  if (!mission) {
    return (
      <div className="bg-surface-dark border border-white/5 p-6 rounded-2xl shadow-xl flex-shrink-0 flex items-center justify-center">
        <span className="text-neutral-500">No active mission.</span>
      </div>
    );
  }

  return (
    <div className="bg-surface-dark border border-white/5 p-6 rounded-2xl shadow-xl flex-shrink-0 relative overflow-y-auto custom-scrollbar max-h-[50%]">
      
      <AnimatePresence>
        {showSuccess && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="absolute inset-x-0 top-0 bg-brand-500/20 text-brand-300 px-4 py-2 font-medium flex items-center justify-center gap-2 border-b border-brand-500/30 backdrop-blur-md z-10"
          >
            <Check className="w-4 h-4" /> Mission Complete! +{mission.xpReward} XP
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex items-center justify-between mb-2 pt-2">
        <h3 className="text-xl font-bold text-white">{mission.title}</h3>
        {mission.lessonText && (
          <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-brand-500/10 text-brand-400 text-xs font-bold uppercase tracking-wider border border-brand-500/20">
            <BookOpen className="w-3 h-3" /> Lesson
          </div>
        )}
      </div>

      <p className="text-neutral-400 text-sm mb-6 leading-relaxed border-b border-white/5 pb-6">
        {mission.story}
      </p>

      {/* READING MODE GATING */}
      {isReadingMode && mission.lessonText ? (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-6"
        >
          <div className="prose prose-invert prose-sm max-w-none text-neutral-300">
            {typeof mission.lessonText === 'string' ? (
              // Simple split for paragraphs since we aren't using a full markdown parser in this component yet
              mission.lessonText.split('\n\n').map((paragraph, i) => (
                <p key={i} className="mb-4">{
                  // Super basic pseudo-markdown bolding for demo
                  paragraph.split('**').map((part, j) => j % 2 === 1 ? <strong key={j} className="text-white">{part}</strong> : part)
                }</p>
              ))
            ) : (
              mission.lessonText
            )}
          </div>
          
          <button 
            onClick={() => setIsReadingMode(false)}
            className="w-full py-3 rounded-xl bg-white/5 hover:bg-white/10 text-white font-medium border border-white/10 transition flex items-center justify-center gap-2"
          >
            I understand, let's start <ChevronRight className="w-4 h-4" />
          </button>
        </motion.div>
      ) : (
        /* OBJECTIVES MODE */
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-4"
        >
          {mission.objectives.map((obj, i) => {
            const isObjComplete = checkObjective(obj.id, repoState);
            return (
              <motion.div 
                layout
                key={obj.id}
                className={`flex items-start gap-4 p-3 rounded-lg border transition-all duration-500 ${isObjComplete ? 'bg-git-branch/10 border-git-branch/30' : 'bg-black/20 border-white/5'}`}
              >
                <div className="mt-0.5 relative">
                  {isObjComplete ? (
                    <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}>
                      <CheckCircle2 className="w-5 h-5 text-git-branch" />
                    </motion.div>
                  ) : (
                    <Circle className="w-5 h-5 text-neutral-600" />
                  )}
                </div>
                <div>
                  <span className={`text-sm font-medium ${isObjComplete ? 'text-neutral-200' : 'text-neutral-400'}`}>
                    {obj.description}
                  </span>
                  {obj.commandRef && !isObjComplete && (
                    <div className="mt-2 flex items-center gap-2 text-xs">
                      <ChevronRight className="w-3 h-3 text-brand-500" />
                      <code className="bg-white/5 px-2 py-1 rounded text-brand-300 font-mono">
                        {obj.commandRef}
                      </code>
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* NEXT MISSION BUTTON */}
      {isComplete && !isReadingMode && (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-6 flex justify-end"
        >
          <button 
            onClick={() => {
              // Quick and dirty next mission logic for prototype
              const nextIds: Record<string, string> = {
                "phase-1-mission-1": "phase-3-mission-1",
              };
              const next = nextIds[mission.id];
              if (next) {
                useGameStore.getState().setActiveMission(next);
                useGitStore.getState().resetRepository();
              } else {
                alert("More missions coming soon!");
              }
            }}
            className="px-6 py-2.5 rounded-full bg-git-branch text-background-dark font-bold text-sm shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:bg-[#0ea5e9] transition-all flex items-center gap-2"
          >
             Next Mission <ChevronRight className="w-4 h-4" />
          </button>
        </motion.div>
      )}

    </div>
  );
}
