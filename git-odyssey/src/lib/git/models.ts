// src/lib/git/models.ts

// Simulated SHA-1 hash generator
export function generateHash(content: string): string {
  // A simple string hash that looks somewhat like a SHA-1 for simulation
  let hash = 0;
  for (let i = 0; i < content.length; i++) {
    const char = content.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  const hex = Math.abs(hash).toString(16).padStart(8, '0');
  // Pad the rest with random hex to make it look like 40 chars
  let fullHash = hex;
  while (fullHash.length < 40) {
    fullHash += Math.floor(Math.random() * 16).toString(16);
  }
  return fullHash;
}

export type GitObjectType = 'blob' | 'tree' | 'commit';

export interface GitObject {
  id: string; // The hash
  type: GitObjectType;
}

export interface BlobObject extends GitObject {
  type: 'blob';
  content: string; // Raw file content
}

export interface TreeEntry {
  mode: string;
  type: 'blob' | 'tree';
  id: string; // Hash of the object
  name: string; // Filename or directory name
}

export interface TreeObject extends GitObject {
  type: 'tree';
  entries: TreeEntry[];
}

export interface CommitObject extends GitObject {
  type: 'commit';
  tree: string; // Hash of the root tree
  parents: string[]; // Hashes of parent commits (0 for initial, 1 for normal, 2+ for merge)
  author: {
    name: string;
    email: string;
    timestamp: number;
  };
  message: string;
}

export interface FileNode {
  type: 'file' | 'dir';
  name: string;
  content?: string; // If file
  children?: Record<string, FileNode>; // If dir
}

// Represents the working directory or staging area structure
export type FileSystemState = Record<string, FileNode>;
