"use client";

import { useState, useEffect } from "react";

export default function TopNav() {
  const [tokensSaved, setTokensSaved] = useState("0");
  const [activeModel, setActiveModel] = useState("gemini-2.0-flash");
  const [isSimpleView, setIsSimpleView] = useState(false);

  // Expose toggle globally so other components can react
  useEffect(() => {
    const handleStorageChange = () => {
      setIsSimpleView(localStorage.getItem('simple_view') === 'true');
      setActiveModel(localStorage.getItem('active_model') || "gemini-2.0-flash");
      setTokensSaved(localStorage.getItem('rag_tokens_saved') || "0");
    };
    
    // Initial fetch
    handleStorageChange();

    // Listen for custom event
    window.addEventListener('storage_update', handleStorageChange);
    return () => window.removeEventListener('storage_update', handleStorageChange);
  }, []);

  const toggleSimpleView = () => {
    const newVal = !isSimpleView;
    setIsSimpleView(newVal);
    localStorage.setItem('simple_view', newVal.toString());
    window.dispatchEvent(new Event('storage_update'));
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shadow-sm">
      <div className="flex items-center gap-4">
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
          PROD Environment
        </span>
        <div className="h-4 w-px bg-slate-300" />
        <span className="text-sm text-slate-500 font-medium flex items-center gap-1.5 cursor-help group relative">
          <span>Active LLM: <span className="text-slate-700">{activeModel}</span></span>
          <span className="text-slate-400">ℹ</span>
          <div className="absolute top-6 left-0 w-64 p-2 bg-slate-800 text-slate-100 text-xs rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
            The foundation model processing the final RAG context. Configurable in Settings.
          </div>
        </span>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex flex-col items-end cursor-help group relative">
          <span className="text-xs text-slate-500 font-medium uppercase tracking-wider">RAG Token Savings</span>
          <span className="text-sm font-bold text-emerald-600">~{parseInt(tokensSaved).toLocaleString()} 🪙</span>
          
          <div className="absolute top-10 right-0 w-72 p-3 bg-slate-800 text-slate-100 text-xs rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
            <p className="font-semibold mb-1">RAG Efficiency Metric</p>
            <p>Estimated tokens saved by retrieving local context vs passing entire documents in the prompt window.</p>
          </div>
        </div>

        <button 
          onClick={toggleSimpleView}
          className="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900 bg-slate-50 px-3 py-1.5 rounded-md border border-slate-200 transition-colors"
        >
          <span>Simple View</span>
          <div className={`w-8 h-4 rounded-full relative transition-colors ${isSimpleView ? 'bg-emerald-500' : 'bg-slate-300'}`}>
            <div className={`w-3 h-3 bg-white rounded-full absolute top-0.5 shadow-sm transition-transform ${isSimpleView ? 'translate-x-4' : 'translate-x-0.5'}`}></div>
          </div>
        </button>
      </div>
    </header>
  );
}
