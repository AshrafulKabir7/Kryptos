import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { Activity, ShieldAlert, Cpu, BarChart3, Clock, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

const SECURITY_DATA = [
  { alg: "Substitution Cipher", cat: "Classical", key: "26! ≈ 4×10²⁶", sec: "~88 bits", attack: "Frequency analysis", status: "Broken", note: "Broken trivially on any text >50 chars" },
  { alg: "Double Transposition", cat: "Classical", key: "n! × m!", sec: "varies", attack: "Brute force / known plaintext", status: "Weak", note: "Preserves letter frequencies; small keys are enumerable" },
  { alg: "DES", cat: "Symmetric", key: "56-bit", sec: "56-bit", attack: "Brute force (1998)", status: "Broken", note: "Cracked in 22 hours in 1999; retired" },
  { alg: "AES-128", cat: "Symmetric", key: "128-bit", sec: "128-bit", attack: "Best: 2¹²⁶ (biclique)", status: "Secure", note: "Current standard; safe for most uses" },
  { alg: "AES-256", cat: "Symmetric", key: "256-bit", sec: "256-bit", attack: "No practical attack known", status: "Secure", note: "Post-quantum candidate; recommended for long-term data" },
  { alg: "RSA-512", cat: "Public-Key", key: "512-bit", sec: "<80-bit", attack: "Factored in weeks (1990s)", status: "Broken", note: "Deprecated; factored with GNFS" },
  { alg: "RSA-1024", cat: "Public-Key", key: "1024-bit", sec: "~80-bit", attack: "Borderline; computationally expensive", status: "Borderline", note: "NIST deprecated in 2013; avoid for new systems" },
  { alg: "RSA-2048", cat: "Public-Key", key: "2048-bit", sec: "~112-bit", attack: "No practical attack known", status: "Secure", note: "Current recommendation; safe until ~2030" },
  { alg: "ECC (demo curve)", cat: "Public-Key", key: "mod 23", sec: "~5-bit", attack: "Trivial brute force", status: "Broken", note: "Demo only; real ECC uses 256-bit+ curves" }
];

export function SecurityAnalysisModule() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const runBenchmark = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/benchmark');
      setResults(res.data.benchmark_results);
    } catch (err: any) {
      setError(err.message || "Failed to run benchmark");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runBenchmark();
  }, []);

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 bg-[#050807] border border-green-500/20 p-6 rounded-xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none"><Activity className="w-24 h-24 text-green-500" /></div>
          <h3 className="text-sm font-bold uppercase tracking-widest text-green-500 mb-2 flex items-center gap-2">
            <Cpu className="w-4 h-4" /> Live Benchmark
          </h3>
          <p className="text-[10px] text-slate-400 font-mono mb-4 leading-relaxed">
            Runs each algorithm 5 times on real input and measures average execution time. RSA key generation is excluded from timing as it involves probabilistic primality testing.
          </p>
          <button 
            onClick={runBenchmark} disabled={loading}
            className="btn-outline w-full py-2 flex justify-center items-center gap-2 border-green-500/30 hover:border-green-500/80 text-[10px]"
          >
            {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}
            {loading ? "RUNNING BENCHMARKS..." : "RUN AGAIN"}
          </button>
          {!loading && results.length > 0 && (
            <div className="mt-3 text-[9px] text-green-400 font-mono flex items-center gap-1.5">
              <ShieldCheck className="w-3 h-3" /> Done - {results.length} benchmarks completed.
            </div>
          )}
        </div>

        <div className="lg:col-span-2 bg-[#0a110e] border border-white/5 p-6 rounded-xl flex flex-col justify-center">
          <h3 className="text-[11px] font-bold uppercase tracking-widest text-slate-300 mb-4 flex items-center gap-2">
            <Clock className="w-3.5 h-3.5" /> About the Benchmark
          </h3>
          <div className="space-y-2 text-[10px] font-mono text-slate-400">
            <div className="grid grid-cols-4 border-b border-white/5 pb-2">
              <div className="text-slate-500 uppercase">Input sizes:</div>
              <div className="col-span-3 text-slate-300">16 bytes and 1 KB plaintext</div>
            </div>
            <div className="grid grid-cols-4 border-b border-white/5 py-2">
              <div className="text-slate-500 uppercase">Rounds:</div>
              <div className="col-span-3 text-slate-300">5 iterations per algorithm, average taken</div>
            </div>
            <div className="grid grid-cols-4 border-b border-white/5 py-2">
              <div className="text-slate-500 uppercase">Metric:</div>
              <div className="col-span-3 text-slate-300">Wall-clock time in milliseconds</div>
            </div>
            <div className="grid grid-cols-4 pt-2">
              <div className="text-slate-500 uppercase">Platform:</div>
              <div className="col-span-3 text-slate-300">Pure Python, no native crypto libs</div>
            </div>
          </div>
          <p className="mt-4 text-[9px] text-slate-500 italic font-sans">Note: results reflect Python overhead, not hardware-optimized performance. Real-world implementations (OpenSSL, etc.) are orders of magnitude faster.</p>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl text-xs flex items-center gap-2">
          <ShieldAlert className="w-4 h-4" /> {error}
        </div>
      )}

      {/* Bar Chart Fake Representation / List */}
      <div className="bg-[#050807] border border-green-500/10 p-6 rounded-xl">
        <h3 className="text-[11px] font-bold uppercase tracking-widest text-slate-300 mb-6 flex items-center gap-2">
          <BarChart3 className="w-3.5 h-3.5 text-green-500" /> Execution Time (ms) - Log Scale
        </h3>
        
        {loading ? (
          <div className="h-64 flex items-center justify-center text-green-500 flex-col gap-3">
            <Loader2 className="w-8 h-8 animate-spin" />
            <span className="text-[10px] uppercase tracking-widest font-bold">Computing Benchmark...</span>
          </div>
        ) : (
          <div className="space-y-3">
            {results.map((r, i) => {
              // Fake log scale calculation for visual bar width
              // Values range from 0.01ms to 300ms roughly.
              // We'll use Math.log10(avg * 100) to get a decent bar width
              let logVal = Math.max(0.5, Math.log10(r.avg * 1000)); 
              let widthPct = Math.min(100, (logVal / 6) * 100);

              return (
                <div key={i} className="flex flex-col gap-1 group">
                  <div className="text-[10px] font-mono text-slate-400 group-hover:text-slate-200 transition-colors">
                    {r.algorithm}
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 bg-black/50 h-3 rounded-sm overflow-hidden border border-white/5">
                      <motion.div 
                        initial={{ width: 0 }} 
                        animate={{ width: `${widthPct}%` }} 
                        transition={{ duration: 1, delay: i * 0.05 }}
                        className="h-full bg-gradient-to-r from-green-500/50 to-green-400/80 rounded-sm"
                      />
                    </div>
                    <div className="w-16 text-right text-[10px] font-mono font-bold text-green-400">
                      {r.avg.toFixed(3)}ms
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Full Results Table */}
      <div className="bg-[#0b100e] border border-white/5 p-6 rounded-xl overflow-x-auto">
        <h3 className="text-[11px] font-bold uppercase tracking-widest text-slate-300 mb-4">Full Results</h3>
        <table className="w-full text-left text-[10px] font-mono">
          <thead>
            <tr className="border-b border-white/10 text-slate-500 uppercase tracking-widest">
              <th className="pb-3 px-2">Algorithm</th>
              <th className="pb-3 px-2">Category</th>
              <th className="pb-3 px-2">Key Size</th>
              <th className="pb-3 px-2">Avg (ms)</th>
              <th className="pb-3 px-2">Min (ms)</th>
              <th className="pb-3 px-2">Max (ms)</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="py-8 text-center text-green-500/50"><Loader2 className="w-5 h-5 animate-spin mx-auto" /></td></tr>
            ) : results.length === 0 ? (
              <tr><td colSpan={6} className="py-8 text-center text-slate-500">No data available.</td></tr>
            ) : results.map((r, i) => (
              <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td className="py-3 px-2 text-slate-300">{r.algorithm}</td>
                <td className="py-3 px-2 text-green-400/80">{r.category}</td>
                <td className="py-3 px-2 text-slate-400">{r.key_size}</td>
                <td className="py-3 px-2 text-green-300 font-bold">{r.avg.toFixed(3)}</td>
                <td className="py-3 px-2 text-slate-500">{r.min.toFixed(3)}</td>
                <td className="py-3 px-2 text-slate-500">{r.max.toFixed(3)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Security Comparison Table */}
      <div className="bg-[#050807] border border-white/5 p-6 rounded-xl overflow-x-auto">
        <h3 className="text-[11px] font-bold uppercase tracking-widest text-slate-300 mb-4 flex items-center gap-2">
          <ShieldAlert className="w-3.5 h-3.5 text-red-500" /> Security Comparison
        </h3>
        <table className="w-full text-left text-[10px] font-sans">
          <thead>
            <tr className="border-b border-white/10 text-slate-500 uppercase tracking-widest font-bold">
              <th className="pb-3 px-2 font-bold">Algorithm</th>
              <th className="pb-3 px-2 font-bold">Category</th>
              <th className="pb-3 px-2 font-bold">Key Size</th>
              <th className="pb-3 px-2 font-bold">Effective Security</th>
              <th className="pb-3 px-2 font-bold">Known Attack</th>
              <th className="pb-3 px-2 font-bold">Status</th>
              <th className="pb-3 px-2 font-bold">Notes</th>
            </tr>
          </thead>
          <tbody className="font-mono">
            {SECURITY_DATA.map((r, i) => (
              <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                <td className="py-3 px-2 text-slate-200 font-bold">{r.alg}</td>
                <td className="py-3 px-2 text-slate-400">{r.cat}</td>
                <td className="py-3 px-2 text-slate-500">{r.key}</td>
                <td className="py-3 px-2 text-slate-300 font-bold">{r.sec}</td>
                <td className="py-3 px-2 text-slate-400">{r.attack}</td>
                <td className={`py-3 px-2 font-bold ${
                  r.status === 'Secure' ? 'text-green-500' :
                  r.status === 'Borderline' ? 'text-yellow-500' : 'text-red-500'
                }`}>
                  {r.status}
                </td>
                <td className="py-3 px-2 text-slate-500 font-sans text-[9px]">{r.note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
