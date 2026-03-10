"use client";

import { useState, useEffect } from "react";
import axios from "axios";

export default function QueryConsole() {
  const [query, setQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [isSimpleView, setIsSimpleView] = useState(false);
  
  const [result, setResult] = useState<{
    answer: string;
    context: string;
    confidence: number;
    tokens: { prompt: number; completion: number; total: number; cost: number };
    latency: { emb: number; ret: number; llm: number; total: number };
  } | null>(null);

  useEffect(() => {
    // Sync with TopNav toggle
    const handleStorageChange = () => {
      setIsSimpleView(localStorage.getItem('simple_view') === 'true');
    };
    handleStorageChange();
    window.addEventListener('storage_update', handleStorageChange);
    return () => window.removeEventListener('storage_update', handleStorageChange);
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsSearching(true);
    setResult(null);

    // Pull the API key from local storage
    const geminiKey = localStorage.getItem('gemini_api_key') || "";
    const openaiKey = localStorage.getItem('openai_api_key') || "";
    const activeModel = localStorage.getItem('active_model') || "gemini-2.0-flash";
    const apiKeyToUse = activeModel.includes('gpt') ? openaiKey : geminiKey;

    try {
      const response = await axios.post("http://localhost:8000/api/v1/query", {
        query: query,
        model: activeModel
      }, {
        params: {
          api_key: apiKeyToUse // Passing the selected key dynamically
        }
      });
      
      const data = response.data;
      
      setResult({
        answer: data.answer,
        context: data.retrieved_context,
        confidence: data.confidence_score,
        tokens: { 
          prompt: data.usage.prompt_tokens, 
          completion: data.usage.completion_tokens, 
          total: data.usage.total_tokens, 
          cost: data.usage.estimated_cost_usd 
        },
        latency: { 
          emb: data.latency_ms.embedding_ms, 
          ret: data.latency_ms.retrieval_ms, 
          llm: data.latency_ms.llm_ms, 
          total: data.latency_ms.total_ms 
        }
      });

      // Update global token savings counter
      const currentSaved = parseInt(localStorage.getItem('rag_tokens_saved') || "0");
      // Assuming a full document prompt would have been ~10,000 tokens on average, 
      // minus the actual prompt tokens used for the retrieved chunk.
      const tokensSavedOnThisQuery = Math.max(0, 10000 - data.usage.prompt_tokens);
      localStorage.setItem('rag_tokens_saved', (currentSaved + tokensSavedOnThisQuery).toString());
      window.dispatchEvent(new Event('storage_update'));
      
    } catch (error: any) {
      console.error(error);
      const errDetail = error.response?.data?.detail || "Failed to process query.";
      alert(`Error: ${errDetail}`);
    } finally {
      setIsSearching(false);
      setQuery(""); // Clear the input box after submission
    }
  };

  return (
    <div className="flex flex-col h-full gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">Query Console</h2>
          <p className="text-sm text-slate-500 mt-1">Interact securely with enterprise documents via Hybrid RAG.</p>
        </div>
        
        <div className="flex gap-2">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            Index: enterprise_docs
          </span>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
            Active
          </span>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col flex-1">
        
        {/* Results Area (Scrollable) */}
        <div className="flex-1 p-6 overflow-y-auto bg-slate-50/50">
          {!result && !isSearching && (
            <div className="h-full flex flex-col items-center justify-center text-slate-400">
              <span className="text-4xl mb-4">🤖</span>
              <p className="text-lg font-medium text-slate-600">How can I help you today?</p>
              <p className="text-sm mt-2 max-w-sm text-center">Ask questions about policies, codebase architecture, or HR guidelines. Answers are grounded strictly in uploaded documents.</p>
            </div>
          )}

          {isSearching && (
            <div className="flex items-center space-x-3 text-slate-500 font-medium my-4">
              <div className="w-4 h-4 rounded-full border-2 border-slate-300 border-t-emerald-600 animate-spin" />
              <span>Retrieving context & generating response...</span>
            </div>
          )}

          {result && !isSearching && (
            <div className="space-y-6 animate-in fade-in duration-500">
              {/* Answer Block */}
              <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm relative">
                <div className="absolute -top-3 left-4 bg-white px-2">
                  <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">AI Answer</span>
                </div>
                {/* Use white-space pre-wrap to respect newlines from the LLM */}
                <p className="text-slate-800 leading-relaxed text-[15px] whitespace-pre-wrap">{result.answer}</p>
                
                {!isSimpleView && (
                  <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center">
                    <div className="flex gap-4">
                      <span className="text-xs text-slate-500 cursor-help" title="Time taken for the entire Hybrid RAG pipeline">
                        ⏱ {result.latency.total}ms
                      </span>
                      <span className="text-xs text-slate-500 cursor-help" title="Cost based on input+output tokens at $1/1M tokens">
                        💰 ${result.tokens.cost.toFixed(6)}
                      </span>
                    </div>
                    <div className="flex gap-2">
                       <button className="text-xs font-medium text-slate-400 hover:text-slate-600 transition-colors">👍 Helpful</button>
                       <button className="text-xs font-medium text-slate-400 hover:text-slate-600 transition-colors ml-2">👎 Inaccurate</button>
                    </div>
                  </div>
                )}
              </div>

              {/* Context Block - Hidden in Simple View */}
              {!isSimpleView && (
                <div className="bg-slate-100 p-5 rounded-lg border border-slate-200">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Retrieved Context</span>
                    <span className="text-xs font-medium bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">
                      {(result.confidence * 100).toFixed(1)}% Match
                    </span>
                  </div>
                  <p className="text-sm text-slate-600 italic leading-relaxed font-serif whitespace-pre-wrap">
                    "{result.context}"
                  </p>
                </div>
              )}

              {/* Dev Metrics Grid - Hidden in Simple View */}
              {!isSimpleView && (
                <div className="grid grid-cols-4 gap-4">
                  <MetricCard label="Prompt Tokens" value={result.tokens.prompt} />
                  <MetricCard label="Completion Tokens" value={result.tokens.completion} />
                  <MetricCard label="Embedding Latency" value={`${result.latency.emb}ms`} />
                  <MetricCard label="Retrieval/LLM Latency" value={`${result.latency.llm+result.latency.ret}ms`} />
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Area (Sticky Bottom) */}
        <div className="p-4 bg-white border-t border-slate-200">
          <form onSubmit={handleSearch} className="relative flex items-center">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything about the enterprise knowledge base..."
              className="w-full bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block p-4 pr-32 shadow-sm placeholder-slate-400 transition-all"
              disabled={isSearching}
            />
            <button
              type="submit"
              disabled={!query.trim() || isSearching}
              className="absolute right-2 top-2 bottom-2 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-md text-sm px-6 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Analyze
            </button>
          </form>
          {!isSimpleView && (
            <div className="flex justify-between items-center mt-2 px-1">
              <span className="text-xs text-slate-400">Strict mode enabled. Answers grounded only in verified context.</span>
              <span className="text-xs text-slate-400">Using: all-MiniLM-L6-v2 + Configured LLM</span>
            </div>
          )}
        </div>
        
      </div>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-white border border-slate-200 rounded p-3 flex flex-col">
      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">{label}</span>
      <span className="text-sm font-semibold text-slate-700">{value}</span>
    </div>
  );
}
