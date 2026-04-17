import { useState } from "react";
import { api } from "@/lib/api";
import { RefreshCw, Repeat, ShieldBan, ShieldCheck, BarChart3 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useFlow } from "@/context/FlowContext";

export function ClassicalModule() {
  const [activeTab, setActiveTab] = useState<"sub" | "trans">("sub");

  return (
    <div className="glass-card p-6 md:p-10 relative overflow-hidden">
      <div className="absolute top-[-50px] right-[-50px] w-64 h-64 bg-green-500/5 blur-[80px] rounded-full pointer-events-none" />

      <div className="mb-10 relative z-10 flex flex-col items-center text-center">
        <h2 className="text-2xl font-black uppercase tracking-widest text-white mb-3">
          Historical <span className="gradient-text-neon">Ciphers</span>
        </h2>
        <p className="text-slate-500 text-xs font-mono max-w-xl leading-relaxed">
          Base-layer substitution and physical transposition frameworks.
        </p>
      </div>

      <div className="flex gap-3 mb-8 relative z-10 justify-center">
        <button onClick={() => setActiveTab("sub")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded border transition-all duration-300 text-xs font-bold uppercase tracking-wider ${activeTab === 'sub' ? 'bg-[#0f1714] text-green-400 border-green-500/20 shadow-[0_0_20px_rgba(34,197,94,0.1)]' : 'bg-transparent text-slate-500 border-white/5 hover:bg-white/[0.02] hover:text-slate-300'}`}>
          <RefreshCw className="w-3.5 h-3.5" /> Substitution
        </button>
        <button onClick={() => setActiveTab("trans")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded border transition-all duration-300 text-xs font-bold uppercase tracking-wider ${activeTab === 'trans' ? 'bg-[#0f1714] text-green-400 border-green-500/20 shadow-[0_0_20px_rgba(34,197,94,0.1)]' : 'bg-transparent text-slate-500 border-white/5 hover:bg-white/[0.02] hover:text-slate-300'}`}>
          <Repeat className="w-3.5 h-3.5" /> Transposition
        </button>
      </div>

      <div className="relative z-10">
        <AnimatePresence mode="wait">
          {activeTab === "sub" ? (
            <motion.div key="sub" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 10 }} transition={{ duration: 0.2 }}>
              <SubstitutionCipher />
            </motion.div>
          ) : (
            <motion.div key="trans" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 10 }} transition={{ duration: 0.2 }}>
              <DoubleTransposition />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

/* ═══ Frequency Analysis Chart Component ═══ */
function FrequencyChart({ frequency }: { frequency: Record<string, number> }) {
  if (!frequency || Object.keys(frequency).length === 0) return null;

  const maxVal = Math.max(...Object.values(frequency), 1);
  const sorted = Object.entries(frequency).sort((a, b) => a[0].localeCompare(b[0]));

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-6">
      <div className="flex items-center gap-2 mb-3">
        <BarChart3 className="w-3.5 h-3.5 text-green-500" />
        <span className="section-label !mb-0 text-green-500">Frequency Analysis</span>
      </div>
      <div className="bg-[#050807] border border-green-500/10 rounded-xl p-4 overflow-x-auto">
        <div className="flex items-end gap-1 min-w-[500px] h-[120px]">
          {sorted.map(([char, count]) => (
            <div key={char} className="flex-1 flex flex-col items-center gap-1 group">
              <span className="text-[8px] font-mono text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity">
                {count}
              </span>
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: `${(count / maxVal) * 80}px` }}
                transition={{ duration: 0.5 }}
                className="w-full bg-gradient-to-t from-green-500/60 to-green-400/30 rounded-t group-hover:from-green-500 group-hover:to-green-400/60 transition-colors min-h-[2px]"
              />
              <span className="text-[9px] font-mono text-slate-400 font-bold">{char}</span>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function SubstitutionCipher() {
  const [text, setText] = useState("");
  const [key, setKey] = useState("QWERTYUIOPASDFGHJKLZXCVBNM");
  const [result, setResult] = useState("");
  const [frequency, setFrequency] = useState<Record<string, number> | null>(null);
  const [lastAction, setLastAction] = useState<string>("");
  const { triggerFlow } = useFlow();

  const handleAction = async (action: "encrypt" | "decrypt") => {
    triggerFlow("substitution", action);
    try {
      const res = await api.post(`/classical/substitution/${action}`, { text, key });
      setResult(action === "encrypt" ? res.data.ciphertext : res.data.plaintext);
      setFrequency(res.data.frequency || null);
      setLastAction(action);
    } catch (err: any) {
      alert("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  // Build key mapping display
  const keyMapping = key.length === 26 ? 
    Array.from({ length: 26 }, (_, i) => ({
      from: String.fromCharCode(65 + i),
      to: key[i] || '?'
    })) : [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Side */}
        <div className="space-y-6 bg-white/[0.01] p-6 rounded-xl border border-white/5">
          <div>
            <div className="section-label">Input 1: Plaintext String</div>
            <textarea placeholder="Enter plaintext message..." value={text} onChange={(e) => setText(e.target.value)} className="textarea-dark h-28" />
          </div>
          <div>
            <div className="section-label flex items-center justify-between">
              <span>Input 2: Key (26-Letter Permutation)</span>
              <span className="text-green-500/50">{key.length}/26</span>
            </div>
            <input type="text" value={key} onChange={(e) => setKey(e.target.value.toUpperCase())} maxLength={26}
              className="input-dark text-green-100 placeholder:text-green-900/40 tracking-widest" />
          </div>

          {/* Key Mapping Display */}
          {keyMapping.length === 26 && (
            <div>
              <div className="section-label">Key Mapping (A→Q, B→W, ...)</div>
              <div className="bg-[#050807] border border-white/5 rounded-lg p-3 grid grid-cols-13 gap-1 max-h-[80px] overflow-y-auto">
                {keyMapping.map((m, i) => (
                  <div key={i} className="text-center">
                    <span className="text-[9px] font-mono text-slate-500 block">{m.from}</span>
                    <span className="text-[8px] text-slate-600">↓</span>
                    <span className="text-[9px] font-mono text-green-400 block font-bold">{m.to}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-4">
            <button onClick={() => handleAction("encrypt")} className="btn-primary w-full flex items-center justify-center gap-2">
              <ShieldCheck className="w-4 h-4" /> Encrypt
            </button>
            <button onClick={() => handleAction("decrypt")} className="btn-outline w-full flex items-center justify-center gap-2">
              <ShieldBan className="w-4 h-4" /> Decrypt
            </button>
          </div>
        </div>

        {/* Output Side */}
        <div className="bg-[#050807] rounded-xl p-6 border border-green-500/10 flex flex-col">
          {result ? (
            <div className="flex-1 flex flex-col gap-4">
              <div>
                <div className="section-label text-green-500">{lastAction === 'encrypt' ? 'Output (Encryption): Ciphertext' : 'Output (Decryption): Original Plaintext'}</div>
                <div className="result-box min-h-[80px]">{result}</div>
              </div>

              {/* Frequency Analysis */}
              {frequency && <FrequencyChart frequency={frequency} />}
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-green-900/40 text-xs font-mono border border-dashed border-green-900/30 rounded-xl min-h-[200px]">
              Awaiting module trigger.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function DoubleTransposition() {
  const [text, setText] = useState("");
  const [key1, setKey1] = useState("FIRSTKEY");
  const [key2, setKey2] = useState("SECONDKEY");
  const [result, setResult] = useState("");
  const [frequency, setFrequency] = useState<Record<string, number> | null>(null);
  const [permKeys, setPermKeys] = useState<{ k1: number[] | null, k2: number[] | null }>({ k1: null, k2: null });
  const [lastAction, setLastAction] = useState<string>("");
  const { triggerFlow } = useFlow();

  const handleAction = async (action: "encrypt" | "decrypt") => {
    triggerFlow("transposition", action);
    try {
      const res = await api.post(`/classical/transposition/${action}`, { text, key1, key2 });
      setResult(action === "encrypt" ? res.data.ciphertext : res.data.plaintext);
      setFrequency(res.data.frequency || null);
      setPermKeys({ k1: res.data.key1_perm || null, k2: res.data.key2_perm || null });
      setLastAction(action);
    } catch (err: any) {
      alert("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Side */}
        <div className="space-y-6 bg-white/[0.01] p-6 rounded-xl border border-white/5">
          <div>
            <div className="section-label">Input 1: Plaintext</div>
            <textarea placeholder="Enter message..." value={text} onChange={(e) => setText(e.target.value)} className="textarea-dark h-24" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="section-label">Input 2: First Permutation Key</div>
              <input type="text" value={key1} onChange={(e) => setKey1(e.target.value.toUpperCase())} className="input-dark text-green-100" />
            </div>
            <div>
              <div className="section-label">Input 3: Second Permutation Key</div>
              <input type="text" value={key2} onChange={(e) => setKey2(e.target.value.toUpperCase())} className="input-dark text-green-100" />
            </div>
          </div>
          <div className="flex gap-4">
            <button onClick={() => handleAction("encrypt")} className="btn-primary w-full flex items-center justify-center gap-2">
              <ShieldCheck className="w-4 h-4" /> Encrypt
            </button>
            <button onClick={() => handleAction("decrypt")} className="btn-outline w-full flex items-center justify-center gap-2">
              <ShieldBan className="w-4 h-4" /> Decrypt
            </button>
          </div>
        </div>

        {/* Output Side */}
        <div className="bg-[#050807] rounded-xl p-6 border border-green-500/10 flex flex-col">
          {result ? (
            <div className="flex-1 flex flex-col gap-4">
              <div>
                <div className="section-label text-green-500">{lastAction === 'encrypt' ? 'Output (Encryption): Permuted Ciphertext' : 'Output (Decryption): Original Plaintext'}</div>
                <div className="result-box min-h-[60px]">{result}</div>
              </div>

              {/* Permutation keys generated */}
              {permKeys.k1 && (
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-white/[0.02] border border-white/5 rounded-lg p-3">
                    <div className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1">Key 1 Permutation</div>
                    <div className="text-xs font-mono text-green-400 tracking-wider">[{permKeys.k1.join(', ')}]</div>
                  </div>
                  {permKeys.k2 && (
                    <div className="bg-white/[0.02] border border-white/5 rounded-lg p-3">
                      <div className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1">Key 2 Permutation</div>
                      <div className="text-xs font-mono text-green-400 tracking-wider">[{permKeys.k2.join(', ')}]</div>
                    </div>
                  )}
                </div>
              )}

              {/* Frequency Analysis */}
              {frequency && <FrequencyChart frequency={frequency} />}
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-green-900/40 text-xs font-mono border border-dashed border-green-900/30 rounded-xl min-h-[200px]">
              Awaiting module trigger.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
