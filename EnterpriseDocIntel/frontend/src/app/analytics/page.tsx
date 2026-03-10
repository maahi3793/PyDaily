"use client";

export default function AnalyticsPage() {
  return (
    <div className="flex flex-col gap-8 max-w-6xl">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">Token Economics & Analytics</h2>
        <p className="text-sm text-slate-500 mt-1">Live metrics demonstrating the cost-efficiency of the Hybrid RAG architecture.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KPICard title="Total Queries" value="1,284" trend="+12% this week" isPositive={true} />
        <KPICard title="Est. Tokens Saved" value="1.4M" trend="vs Full Prompting" isPositive={true} highlight={true} />
        <KPICard title="RAG Efficiency Score" value="94.2%" trend="Top Decile" isPositive={true} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Mock Chart Area */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col h-80">
          <h3 className="text-sm font-bold text-slate-900 mb-4">Token Consumption (7 Days)</h3>
          <div className="flex-1 flex items-end gap-2 pt-4">
            {/* Simple CSS bar chart mock */}
            {[40, 25, 60, 30, 80, 45, 90].map((h, i) => (
              <div key={i} className="flex-1 flex flex-col justify-end gap-2 group">
                 <div className="w-full bg-slate-100 rounded-t-sm relative flex flex-col justify-end h-full">
                    {/* Saved Tokens portion (imagined overlay) */}
                    <div className="w-full bg-emerald-100 border-t border-emerald-200 opacity-50 absolute bottom-0" style={{height: `${h*1.5}%`, maxHeight: '100%'}} />
                    {/* Used Tokens */}
                    <div className="w-full bg-blue-500 rounded-t-sm relative z-10 transition-all group-hover:bg-blue-600" style={{height: `${h}%`}} />
                 </div>
                 <span className="text-[10px] text-slate-400 text-center">Day {i+1}</span>
              </div>
            ))}
          </div>
          <div className="flex justify-center gap-6 mt-4">
            <div className="flex items-center gap-2 text-xs text-slate-500"><div className="w-3 h-3 bg-blue-500 rounded-sm" /> Tokens Consumed (LLM)</div>
            <div className="flex items-center gap-2 text-xs text-slate-500"><div className="w-3 h-3 bg-emerald-100 border border-emerald-200 rounded-sm" /> Tokens Prevented (RAG)</div>
          </div>
        </div>

        {/* Latency Breakdown Area */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col h-80">
          <h3 className="text-sm font-bold text-slate-900 mb-4 border-b border-slate-100 pb-2">Average Request Latency (ms)</h3>
          
          <div className="flex-1 w-full flex flex-col justify-center gap-6">
            <LatencyBar label="1. Local CPU Embedding (all-MiniLM-L6-v2)" ms={45} limit={3000} color="bg-indigo-500" />
            <LatencyBar label="2. Local Vector Search (ChromaDB)" ms={12} limit={3000} color="bg-violet-500" />
            <LatencyBar label="3. Cloud LLM Generation (Gemini 2.0 Flash)" ms={1450} limit={3000} color="bg-emerald-500" />
            
            <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center">
              <span className="text-sm font-bold text-slate-700">Total Roundtrip:</span>
              <span className="text-xl font-bold text-slate-900">1,507 ms</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function KPICard({ title, value, trend, isPositive, highlight = false }: any) {
  return (
    <div className={`p-6 rounded-xl border ${highlight ? 'bg-emerald-50 border-emerald-200 shadow-sm' : 'bg-white border-slate-200 shadow-sm'}`}>
      <h3 className={`text-sm font-medium ${highlight ? 'text-emerald-800' : 'text-slate-500'}`}>{title}</h3>
      <div className="mt-2 flex items-baseline gap-2">
        <span className={`text-3xl font-bold tracking-tight ${highlight ? 'text-emerald-900' : 'text-slate-900'}`}>{value}</span>
        <span className={`text-sm font-medium ${isPositive ? 'text-emerald-600' : 'text-red-600'}`}>
          {trend}
        </span>
      </div>
    </div>
  );
}

function LatencyBar({ label, ms, limit, color }: any) {
  const width = Math.max(2, (ms / limit) * 100);
  return (
    <div className="w-full">
      <div className="flex justify-between text-xs mb-1">
        <span className="font-medium text-slate-700">{label}</span>
        <span className="text-slate-500">{ms} ms</span>
      </div>
      <div className="w-full bg-slate-100 rounded-full h-2">
        <div className={`h-2 rounded-full ${color} transition-all duration-1000`} style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}
