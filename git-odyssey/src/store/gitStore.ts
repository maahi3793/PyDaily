import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { GitEngine, RepositoryState } from '@/lib/git/engine';
import { executeGitCommand, CommandResult } from '@/lib/git/parser';

interface GitStore {
  // Underlying state
  repoState: RepositoryState;
  
  // Terminal History
  terminalHistory: { command: string; output: string; error?: boolean }[];

  // Actions
  dispatchCommand: (command: string) => CommandResult;
  simulateFileEdit: (path: string, content: string) => void;
  resetRepository: () => void;
}

export const useGitStore = create<GitStore>()(
  persist(
    (set, get) => ({
      repoState: new GitEngine().getState(),
      terminalHistory: [
        { command: '', output: 'Welcome to Git Odyssey! Type "git init" to begin.' }
      ],

      dispatchCommand: (command: string) => {
        const trimmed = command.trim();
        
        // Handle native terminal commands first
        if (trimmed === 'clear') {
          set({
            terminalHistory: []
          });
          return { output: "" };
        }

        // Hydrate engine with current state
        const engine = new GitEngine(get().repoState);
        
        // Execute
        const result = executeGitCommand(engine, command);
        
        // Save history and new state
        set((state) => ({
          repoState: engine.getState(),
          terminalHistory: [
            ...state.terminalHistory,
            { command, output: result.output, error: result.error }
          ]
        }));

        return result;
      },

      simulateFileEdit: (path: string, content: string) => {
        const engine = new GitEngine(get().repoState);
        engine.writeFile(path, content);
        set({ repoState: engine.getState() });
      },

      resetRepository: () => {
        set({
          repoState: new GitEngine().getState(),
          terminalHistory: [
            { command: '', output: 'Repository reset. Type "git init" to begin.' }
          ]
        });
      }
    }),
    {
      name: 'git-odyssey-storage',
      // We only persist the repository state and terminal history
    }
  )
);
