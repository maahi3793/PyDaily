import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface Objective {
  id: string;
  description: string;
  commandRef?: string;
}

export interface Mission {
  id: string;
  title: string;
  story: string;
  lessonText?: React.ReactNode | string; // Pre-requisite reading material
  objectives: Objective[];
  hints: string[];
  xpReward: number;
}

interface GameStore {
  xp: number;
  level: number;
  completedMissions: string[];
  activeMissionId: string | null;
  
  // Actions
  addXp: (amount: number) => void;
  completeMission: (missionId: string) => void;
  setActiveMission: (missionId: string) => void;
  resetProgress: () => void;
}

export const useGameStore = create<GameStore>()(
  persist(
    (set) => ({
      xp: 0,
      level: 1,
      completedMissions: [],
      activeMissionId: 'phase-1-mission-1', // Genesis is default

      addXp: (amount: number) => set((state) => {
        const newXp = state.xp + amount;
        const newLevel = Math.floor(newXp / 500) + 1; // 500 XP per level
        return { xp: newXp, level: newLevel };
      }),

      completeMission: (missionId: string) => set((state) => {
        if (!state.completedMissions.includes(missionId)) {
          return { completedMissions: [...state.completedMissions, missionId] };
        }
        return state;
      }),

      setActiveMission: (missionId: string) => set({ activeMissionId: missionId }),

      resetProgress: () => set({
        xp: 0,
        level: 1,
        completedMissions: [],
        activeMissionId: 'phase-1-mission-1'
      })
    }),
    {
      name: 'git-odyssey-progress'
    }
  )
);
