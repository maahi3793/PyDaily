import { Mission } from '@/store/gameStore';

export const ALL_MISSIONS: Mission[] = [
  {
    id: "phase-1-mission-1",
    title: "The Genesis",
    story: "Every great project starts somewhere. You need a space to track your files before you can begin version controlling them.",
    lessonText: `
Git is a Version Control System (VCS). Think of it as a time machine for your code. It takes "snapshots" of your project so you can always go back to an older version.

To start using Git, you must first initialize a repository in your project folder using \`git init\`.

Once initialized, Git starts watching your files but doesn't track them yet. You must tell Git which files to bundle into the next snapshot using \`git add <file>\` (or \`git add .\` for all files).

Finally, you save the snapshot permanently into your timeline using \`git commit -m "your message"\`.
`,
    objectives: [
      { id: "init", description: "Initialize a new Git repository.", commandRef: "git init" },
      { id: "add", description: "Stage the new files in your working directory.", commandRef: "git add ." },
      { id: "commit", description: "Commit with message 'first commit'.", commandRef: "git commit -m 'first commit'" }
    ],
    hints: [
      "Try typing 'git init' to start a new repository.",
      "The simulator has some internal files ready to be added. Use 'git add .' to stage them.",
      "Save your staged files into history using 'git commit -m \"message\"'."
    ],
    xpReward: 100
  },
  {
    id: "phase-3-mission-1",
    title: "Branching Out",
    story: "You want to add a login feature, but you shouldn't break the main project. Create an isolated environment to work in.",
    lessonText: `
A **branch** represents an independent line of development. By default, your main repository line is called \`main\` or \`master\`.

If you want to build a risky new feature (like a login page), you shouldn't build it on the main branch! If it breaks, your whole app breaks.

Instead, you use \`git branch <branch-name>\` to create a new alternate timeline. You then use \`git checkout <branch-name>\` to switch your terminal into that new timeline. Any commits you make now will not affect the main branch!
`,
    objectives: [
      { id: "branch", description: "Create a new branch named 'feature-login'.", commandRef: "git branch feature-login" },
      { id: "checkout", description: "Switch to your new branch.", commandRef: "git checkout feature-login" },
      { id: "commit", description: "Make a commit on the new branch.", commandRef: "git commit -m 'added login'" }
    ],
    hints: [
      "Use 'git branch <name>' to create a branch.",
      "Use 'git checkout <name>' to switch to it.",
      "Don't strictly need to add files in the simulator right now, just try 'git commit -m \"added login\"'."
    ],
    xpReward: 150
  }
];

export function getMissionById(id: string): Mission | undefined {
  return ALL_MISSIONS.find((m) => m.id === id);
}
