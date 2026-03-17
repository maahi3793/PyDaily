// src/lib/git/parser.ts
import { GitEngine } from './engine';

export interface CommandResult {
  output: string;
  error?: boolean;
}

/**
 * Parses a raw user string (e.g., "git commit -m 'hello'") and 
 * executes the appropriate method on the GitEngine.
 */
export function executeGitCommand(engine: GitEngine, input: string): CommandResult {
  const trimmed = input.trim();
  if (!trimmed) return { output: "" };

  const parts = trimmed.split(/\s+/);
  if (parts[0] !== 'git') {
    return { output: `bash: ${parts[0]}: command not found`, error: true };
  }

  const command = parts[1];
  const args = parts.slice(2);

  try {
    switch (command) {
      case 'init':
        return { output: engine.init() };

      case 'add':
        if (args.length === 0) {
          return { output: "Nothing specified, nothing added.", error: true };
        }
        return { output: engine.add(args[0]) };

      case 'commit':
        let message = "Commit message";
        const mIndex = args.indexOf('-m');
        if (mIndex !== -1 && args.length > mIndex + 1) {
          // Extract quoted string or just next word
          const possibleMsg = args.slice(mIndex + 1).join(" ");
          // Simple unquote
          message = possibleMsg.replace(/^["'](.*)["']$/, '$1');
        } else {
            return {
                output: "Aborting commit due to empty commit message.\n(In this simulator, please use git commit -m 'message')",
                error: true
            };
        }
        const { output: commitOut } = engine.commit(message);
        return { output: commitOut };

      case 'branch':
        if (args.length === 0) {
            // Simplified: just list branches
            const state = engine.getState();
            const branches = Object.keys(state.refs)
              .filter(k => k.startsWith('refs/heads/'))
              .map(k => k.replace('refs/heads/', ''));
            const currentHead = state.head.replace('refs/heads/', '');
            return { 
                output: branches.map(b => (b === currentHead ? `* ${b}` : `  ${b}`)).join('\n')
            };
        } else {
            return { output: engine.branch(args[0]) };
        }

      case 'checkout':
      case 'switch':
        if (args.length === 0) {
          return { output: "fatal: missing branch name or commit hash", error: true };
        }
        if (args[0] === '-b' || args[0] === '-c') { // -c for switch, -b for checkout
            if (!args[1]) return { output: "fatal: missing branch name", error: true };
            engine.branch(args[1]);
            return { output: engine.checkout(args[1]) };
        }
        return { output: engine.checkout(args[0]) };

      case 'status':
        // Simplified status
        const s = engine.getState();
        let statusOut = `On branch ${s.head.replace('refs/heads/', '')}\n`;
        const indexKeys = Object.keys(s.index);
        if (indexKeys.length > 0) {
            statusOut += `Changes to be committed:\n`;
            indexKeys.forEach(k => {
                statusOut += `  (new file) ${k}\n`;
            });
        } else {
            statusOut += `nothing to commit, working tree clean`;
        }
        return { output: statusOut };

      case 'log':
        // Simplified linear log
        const logMap = [];
        let currHash = engine.getHeadCommitHash();
        const objState = engine.getState().objects;
        
        while (currHash && objState[currHash]) {
            const commit = objState[currHash] as any;
            if (commit.type !== 'commit') break;
            logMap.push(`commit ${currHash}\nAuthor: ${commit.author.name} <${commit.author.email}>\n\n    ${commit.message}\n`);
            currHash = commit.parents[0]; // Just follow first parent for now
        }
        if (logMap.length === 0) {
            return { output: "fatal: your current branch does not have any commits yet", error: true };
        }
        return { output: logMap.join('\n') };

      default:
        return { output: `git: '${command}' is not a git command. See 'git --help'.`, error: true };
    }
  } catch (err: any) {
    return { output: err.message, error: true };
  }
}
