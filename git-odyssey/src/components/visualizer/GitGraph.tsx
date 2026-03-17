"use client";

import { useGitStore } from '@/store/gitStore';
import { motion, AnimatePresence } from 'framer-motion';
import { useMemo } from 'react';
import { CommitObject } from '@/lib/git/models';

interface Node {
  hash: string;
  commit: CommitObject;
  x: number;
  y: number;
  branches: string[];
  isHead: boolean;
}

export function GitGraph() {
  const repoState = useGitStore((state) => state.repoState);

  // Very simplified graph layout algorithm for a linear history layout.
  // Real implementation would handle multiple lanes and merge commits.
  const graphNodes = useMemo(() => {
    const nodes: Node[] = [];
    const objKeys = Object.keys(repoState.objects);
    
    // Find commits
    const commits = objKeys
      .map(k => ({ hash: k, commit: repoState.objects[k] as CommitObject }))
      .filter(item => item.commit.type === 'commit');

    // Sort by timestamp if available or just linear mapping
    commits.sort((a, b) => a.commit.author.timestamp - b.commit.author.timestamp);

    commits.forEach((item, index) => {
      // Find what branches point here
      const branches = Object.keys(repoState.refs)
        .filter(ref => repoState.refs[ref] === item.hash)
        .map(ref => ref.replace('refs/heads/', ''));

      // Check if HEAD points here directly or via branch
      let isHead = repoState.head === item.hash;
      if (repoState.head.startsWith('refs/heads/')) {
        isHead = repoState.refs[repoState.head] === item.hash;
      }

      nodes.push({
        hash: item.hash,
        commit: item.commit,
        x: 0, // All on one lane for now
        y: index * 80, // 80px apart
        branches,
        isHead
      });
    });

    return nodes;
  }, [repoState]);

  if (graphNodes.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-neutral-500 font-mono text-sm border-2 border-dashed border-white/5 rounded-2xl m-6 bg-black/20">
        <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-neutral-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        No commits yet. <br /> Type `git commit` to create your first node.
      </div>
    );
  }

  return (
    <div className="flex-1 relative overflow-auto p-8 custom-scrollbar bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-surface-dark/50 to-background-dark">
      <div className="relative min-w-[300px]" style={{ height: `${graphNodes.length * 80 + 100}px` }}>
        
        {/* Draw connection lines */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
          {graphNodes.map((node, i) => {
            if (i === 0) return null;
            // Draw line to previous node
            const prev = graphNodes[i - 1];
            return (
              <motion.line
                key={`line-${node.hash}`}
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 1 }}
                transition={{ duration: 0.5 }}
                x1={prev.x + 40 + 12} // offset for left margin + radius
                y1={prev.y + 40}
                x2={node.x + 40 + 12}
                y2={node.y + 40}
                stroke="#3f3f46"
                strokeWidth={4}
              />
            );
          })}
        </svg>

        {/* Draw Commit Nodes */}
        <AnimatePresence>
          {graphNodes.map((node) => (
            <motion.div
              key={node.hash}
              initial={{ scale: 0, opacity: 0, y: 50 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              className="absolute left-[40px] flex items-center gap-6"
              style={{ top: `${node.y + 28}px` }}
            >
              {/* The Dot */}
              <div className={`w-6 h-6 rounded-full border-4 z-10 transition-colors duration-300 ${node.isHead ? 'border-git-head bg-background-dark shadow-[0_0_15px_rgba(236,72,153,0.5)]' : 'border-git-commit bg-background-dark hover:bg-git-commit cursor-pointer'}`} />
              
              {/* Details */}
              <div className="flex flex-col">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-xs text-neutral-400 font-medium px-2 py-0.5 rounded bg-white/5 border border-white/10">
                    {node.hash.substring(0, 7)}
                  </span>
                  
                  {/* Branch Labels */}
                  {node.branches.map(b => (
                    <span key={b} className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-git-branch/20 text-git-branch border border-git-branch/30">
                      {b}
                    </span>
                  ))}
                  
                  {/* HEAD Label */}
                  {node.isHead && (
                    <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-git-head/20 text-git-head border border-git-head/30 shadow-[0_0_10px_rgba(236,72,153,0.2)]">
                      HEAD
                    </span>
                  )}
                </div>
                <div className="text-white font-medium text-sm mt-1 filter drop-shadow-md">
                  {node.commit.message}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

      </div>
    </div>
  );
}
