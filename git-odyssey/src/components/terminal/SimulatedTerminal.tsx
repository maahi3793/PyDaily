"use client";

import { useState, useRef, useEffect } from 'react';
import { useGitStore } from '@/store/gitStore';
import { Terminal } from 'lucide-react';

export default function SimulatedTerminal() {
  const [input, setInput] = useState('');
  const [mounted, setMounted] = useState(false);
  
  const terminalHistory = useGitStore((state) => state.terminalHistory);
  const dispatchCommand = useGitStore((state) => state.dispatchCommand);
  const repoState = useGitStore((state) => state.repoState);
  
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [terminalHistory]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && input.trim() !== '') {
      dispatchCommand(input);
      setInput('');
    }
  };

  if (!mounted) return <div className="h-full bg-black/50 animate-pulse rounded-xl" />;

  const currentBranch = repoState.head.replace('refs/heads/', '');

  return (
    <div className="flex flex-col h-full bg-[#0d0d0f] border border-white/10 rounded-xl overflow-hidden shadow-2xl font-mono text-sm relative">
      {/* Terminal Header */}
      <div className="flex items-center gap-2 px-4 py-3 bg-white/5 border-b border-white/5 select-none">
        <div className="w-3 h-3 rounded-full bg-red-500/80" />
        <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
        <div className="w-3 h-3 rounded-full bg-green-500/80" />
        <span className="ml-4 text-neutral-400 text-xs flex items-center gap-2 font-sans font-medium">
          <Terminal className="w-4 h-4" /> Terminal
        </span>
      </div>

      {/* Terminal View area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 text-neutral-300 custom-scrollbar pb-16">
        {terminalHistory.map((entry, idx) => (
          <div key={idx} className="space-y-1">
            {/* Command typed */}
            {entry.command && (
              <div className="flex items-center gap-2 text-neutral-400">
                <span className="text-brand-400">~/git-odyssey</span> $ {entry.command}
              </div>
            )}
            
            {/* Output */}
            {entry.output && (
              <div className={`whitespace-pre-wrap pl-2 border-l-2 ${entry.error ? 'border-red-500 text-red-400' : 'border-neutral-700 text-neutral-300'}`}>
                {entry.output}
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input area fixed at bottom */}
      <div className="absolute bottom-0 inset-x-0 bg-[#0d0d0f] p-4 flex items-center gap-2 border-t border-white/5 z-20">
        <span className="text-brand-400 whitespace-nowrap">~/git-odyssey <span className="text-git-branch">({currentBranch.substring(0,10) || 'detached'})</span> $</span>
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          className="flex-1 bg-transparent border-none outline-none text-white font-mono w-full"
          placeholder="Type 'git init' to begin"
          autoFocus
           spellCheck="false"
          autoComplete="off"
        />
      </div>
    </div>
  );
}
