// src/lib/git/engine.ts
import { 
  GitObject, BlobObject, TreeObject, CommitObject,
  FileSystemState, generateHash, FileNode 
} from './models';

/**
 * Encapsulates the state of a single Git repository.
 */
export interface RepositoryState {
  objects: Record<string, GitObject>; // .git/objects
  refs: Record<string, string>;       // .git/refs (e.g. "refs/heads/main" -> commit_hash)
  head: string;                       // .git/HEAD (can be a ref name or detached hash)
  index: FileSystemState;             // Staging area (.git/index)
  workingDirectory: FileSystemState;  // The actual files on disk Simulator
  config: {
    userName: string;
    userEmail: string;
  };
}

export class GitEngine {
  private state: RepositoryState;

  constructor(initialState?: RepositoryState) {
    if (initialState) {
      this.state = JSON.parse(JSON.stringify(initialState));
    } else {
      this.state = {
        objects: {},
        refs: {},
        head: '',
        index: {},
        workingDirectory: {},
        config: {
          userName: 'Odyssey Learner',
          userEmail: 'learner@gitodyssey.com'
        }
      };
    }
  }

  getState(): RepositoryState {
    return this.state;
  }

  // --- CORE COMMANDS ---

  public init() {
    this.state.refs['refs/heads/main'] = '';
    this.state.head = 'refs/heads/main';
    
    // Automatically populate some files in the working directory 
    // down so the beginner actually has something to `git add` and `git commit`
    this.writeFile('index.html', '<!DOCTYPE html>\n<html>\n<head>\n  <title>Odyssey</title>\n</head>\n<body>\n  <h1>Hello Git</h1>\n</body>\n</html>');
    this.writeFile('styles.css', 'body {\n  background-color: #000;\n  color: #fff;\n}');
    this.writeFile('README.md', '# My First Project\nLearning Git via Odyssey.');

    return "Initialized empty Git repository.";
  }

  // Helper to resolve HEAD to a commit hash
  public resolveRef(ref: string): string {
    if (this.state.refs[ref] !== undefined) {
      return this.state.refs[ref];
    }
    // If it's a hash
    if (this.state.objects[ref]) {
      return ref;
    }
    return '';
  }

  public getHeadCommitHash(): string {
    const headTarget = this.state.head;
    if (headTarget.startsWith('refs/')) {
      return this.state.refs[headTarget] || '';
    }
    return headTarget; // Detached HEAD
  }

  public getHeadCommit(): CommitObject | null {
    const hash = this.getHeadCommitHash();
    if (!hash) return null;
    return this.state.objects[hash] as CommitObject;
  }

  // Simplified file operations for the simulator
  public writeFile(path: string, content: string) {
    // For simplicity in v1, we assume all files are in root
    this.state.workingDirectory[path] = {
      type: 'file',
      name: path,
      content: content
    };
    return `Created ${path}`;
  }

  // "git add"
  public add(path: string) {
    if (path === '.') {
      // Add all
      this.state.index = JSON.parse(JSON.stringify(this.state.workingDirectory));
      return "";
    }
    
    if (this.state.workingDirectory[path]) {
      this.state.index[path] = JSON.parse(JSON.stringify(this.state.workingDirectory[path]));
      return "";
    } else {
      throw new Error(`fatal: pathspec '${path}' did not match any files`);
    }
  }

  // "git commit"
  public commit(message: string): { hash: string; output: string } {
    if (Object.keys(this.state.index).length === 0 && !this.getHeadCommit()) {
      throw new Error("nothing to commit (create/copy files and use \"git add\" to track)");
    }

    // 1. Create Blobs for files in index
    const treeEntries = [];
    for (const [path, node] of Object.entries(this.state.index)) {
      if (node.type === 'file' && node.content !== undefined) {
        const hash = generateHash(node.content);
        const blob: BlobObject = { id: hash, type: 'blob', content: node.content };
        this.state.objects[hash] = blob;
        treeEntries.push({
          mode: '100644',
          type: 'blob',
          id: hash,
          name: path
        });
      }
    }

    // 2. Create Tree
    const treeContent = JSON.stringify(treeEntries);
    const treeHash = generateHash("tree " + treeContent);
    const tree: TreeObject = {
      id: treeHash,
      type: 'tree',
      entries: treeEntries as any
    };
    this.state.objects[treeHash] = tree;

    // 3. Create Commit
    const parentHash = this.getHeadCommitHash();
    const commitString = `tree ${treeHash}\nparent ${parentHash}\n\n${message}`;
    const commitHash = generateHash("commit " + commitString);
    
    const commit: CommitObject = {
      id: commitHash,
      type: 'commit',
      tree: treeHash,
      parents: parentHash ? [parentHash] : [],
      author: {
        name: this.state.config.userName,
        email: this.state.config.userEmail,
        timestamp: Date.now()
      },
      message
    };
    this.state.objects[commitHash] = commit;

    // 4. Update Reference
    if (this.state.head.startsWith('refs/')) {
      this.state.refs[this.state.head] = commitHash;
    } else {
      // Detached head just moves to new commit
      this.state.head = commitHash;
    }

    const shortHash = commitHash.substring(0, 7);
    return {
      hash: commitHash,
      output: `[${this.state.head.replace('refs/heads/', '')} ${shortHash}] ${message}`
    };
  }

  // "git branch <name>"
  public branch(name: string) {
    const headHash = this.getHeadCommitHash();
    if (!headHash) {
      throw new Error(`fatal: Not a valid object name: '${this.state.head}'.`);
    }
    const refPath = `refs/heads/${name}`;
    if (this.state.refs[refPath]) {
      throw new Error(`fatal: A branch named '${name}' already exists.`);
    }
    this.state.refs[refPath] = headHash;
    return "";
  }

  // "git checkout <name>"
  public checkout(name: string) {
    const refPath = `refs/heads/${name}`;
    if (this.state.refs[refPath] !== undefined) {
      this.state.head = refPath;
      return `Switched to branch '${name}'`;
    }
    
    // Check if it's a commit hash
    if (this.state.objects[name] && this.state.objects[name].type === 'commit') {
      this.state.head = name;
      return `Note: switching to '${name}'.\n\nYou are in 'detached HEAD' state.`;
    }

    // Try partial hash
    const fullHash = Object.keys(this.state.objects).find(h => h.startsWith(name) && this.state.objects[h].type === 'commit');
    if (fullHash) {
      this.state.head = fullHash;
      return `Note: switching to '${name}'.\n\nYou are in 'detached HEAD' state.`;
    }

    throw new Error(`error: pathspec '${name}' did not match any file(s) known to git`);
  }
}
