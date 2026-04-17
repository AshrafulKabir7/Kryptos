import { useState } from "react";
import { api } from "@/lib/api";
import { ShieldBan, ShieldCheck, KeyRound } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useFlow } from "@/context/FlowContext";

export function SymmetricModule() {
  const [activeTab, setActiveTab] = useState<"aes" | "des">("aes");

  return (
    <div className="glass-card p-6 md:p-10 relative overflow-hidden">
      <div className="absolute top-[-50px] right-[-50px] w-64 h-64 bg-green-500/5 blur-[80px] rounded-full pointer-events-none" />

      <div className="mb-10 relative z-10 flex flex-col items-center text-center">
        <h2 className="text-2xl font-black uppercase tracking-widest text-white mb-3">
          Symmetric <span className="gradient-text-neon">Standards</span>
        </h2>
        <p className="text-slate-500 text-xs font-mono max-w-xl leading-relaxed">
          Advanced block ciphers relying on a single shared secret key. Round keys are generated automatically.
        </p>
      </div>

      <div className="flex gap-3 mb-8 relative z-10 justify-center">
        <button onClick={() => setActiveTab("aes")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded border transition-all duration-300 text-xs font-bold uppercase tracking-wider ${activeTab === 'aes' ? 'bg-[#0f1714] text-green-400 border-green-500/20 shadow-[0_0_20px_rgba(34,197,94,0.1)]' : 'bg-transparent text-slate-500 border-white/5 hover:bg-white/[0.02] hover:text-slate-300'}`}>
          AES-128
        </button>
        <button onClick={() => setActiveTab("des")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded border transition-all duration-300 text-xs font-bold uppercase tracking-wider ${activeTab === 'des' ? 'bg-[#0f1714] text-green-400 border-green-500/20 shadow-[0_0_20px_rgba(34,197,94,0.1)]' : 'bg-transparent text-slate-500 border-white/5 hover:bg-white/[0.02] hover:text-slate-300'}`}>
          DES (Data Encryption Standard)
        </button>
      </div>

      <div className="relative z-10">
        <AnimatePresence mode="wait">
          {activeTab === "aes" ? (
            <motion.div key="aes" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 10 }} transition={{ duration: 0.2 }}>
              <SymmetricAlgorithm endpoint="/symmetric/aes" name="AES-128" flowId="aes" />
            </motion.div>
          ) : (
            <motion.div key="des" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 10 }} transition={{ duration: 0.2 }}>
              <SymmetricAlgorithm endpoint="/symmetric/des" name="DES" flowId="des" />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function SymmetricAlgorithm({ endpoint, name, flowId }: { endpoint: string, name: string, flowId: string }) {
  const [text, setText] = useState("");
  const [keyHex, setKeyHex] = useState("");
  const [ciphertextHex, setCiphertextHex] = useState("");
  const [decryptedText, setDecryptedText] = useState("");
  const [roundKeys, setRoundKeys] = useState<string[]>([]);
  const { triggerFlow } = useFlow();
  
  const handleEncrypt = async () => {
    triggerFlow(flowId, "encrypt");
    try {
      const res = await api.post(`${endpoint}/encrypt`, { text });
      setCiphertextHex(res.data.ciphertext_hex);
      setKeyHex(res.data.key_hex);
      setRoundKeys(res.data.round_keys || []);
      setDecryptedText("");
    } catch (err: any) {
      alert("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleDecrypt = async () => {
    if (!keyHex || !ciphertextHex) {
      alert("Please encrypt first to generate a key and ciphertext, or enter them manually.");
      return;
    }
    triggerFlow(flowId, "decrypt");
    try {
      const res = await api.post(`${endpoint}/decrypt`, { 
        ciphertext_hex: ciphertextHex, 
        key_hex: keyHex 
      });
      setDecryptedText(res.data.plaintext);
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
            <textarea 
              placeholder={`Enter plaintext message to encrypt with ${name}...`} 
              value={text} 
              onChange={(e) => setText(e.target.value)} 
              className="textarea-dark h-28"
            />
          </div>
          <div>
            <div className="section-label flex items-center gap-2">
              <KeyRound className="w-3 h-3 text-green-500/50" />
              Input 2: Key (Auto-Generated)
            </div>
            <input 
              type="text"
              value={keyHex} 
              onChange={(e) => setKeyHex(e.target.value.toUpperCase())}
              className="input-dark text-green-100 placeholder:text-green-900/40 tracking-widest"
              placeholder="Key will be auto-generated on encrypt..."
            />
            <p className="text-[9px] text-slate-600 font-mono mt-1">Key is randomly generated during encryption. For decryption, paste the key here.</p>
          </div>
          <div className="flex gap-4">
            <button onClick={handleEncrypt} className="btn-primary w-full flex items-center justify-center gap-2">
              <ShieldCheck className="w-4 h-4" /> Encrypt ({name})
            </button>
            <button onClick={handleDecrypt} className="btn-outline w-full flex items-center justify-center gap-2">
              <ShieldBan className="w-4 h-4" /> Decrypt
            </button>
          </div>
        </div>

        {/* Output Side */}
        <div className="bg-[#050807] rounded-xl p-6 border border-green-500/10 flex flex-col">
          {(ciphertextHex || decryptedText) ? (
            <div className="flex-1 flex flex-col gap-5">
              
              {/* Ciphertext Output */}
              {ciphertextHex && (
                <div>
                  <div className="section-label text-green-500">Output (Encryption): Ciphertext</div>
                  <div className="result-box text-green-300 min-h-[50px]">{ciphertextHex}</div>
                </div>
              )}

              {/* Key Output */}
              {keyHex && (
                <div>
                  <div className="section-label text-green-500/70">Output: Generated Key (Hex)</div>
                  <div className="bg-green-500/5 border border-green-500/15 rounded-lg p-3 font-mono text-xs text-green-300 tracking-wider break-all select-all">
                    {keyHex}
                  </div>
                </div>
              )}

              {/* Decrypted Text Output */}
              {decryptedText && (
                <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }}>
                  <div className="section-label text-amber-500">Output (Decryption): Original Plaintext</div>
                  <div className="bg-amber-500/5 border border-amber-500/20 rounded-lg p-4 text-white font-medium text-sm">
                    {decryptedText}
                  </div>
                </motion.div>
              )}

              {/* Round Keys Output */}
              {roundKeys.length > 0 && (
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="section-label !mb-0 text-green-500/70">Output (Key): All Round Keys</span>
                    <span className="text-[10px] bg-green-500/10 border border-green-500/20 px-1.5 py-0.5 rounded text-green-500 font-mono">{roundKeys.length} Rounds</span>
                  </div>
                  <div className="round-key-terminal">
                    {roundKeys.map((rk, i) => (
                      <div key={i} className="flex gap-3 hover:bg-green-500/10 px-2 py-0.5 rounded transition-colors group">
                        <span className="opacity-40 group-hover:opacity-100 min-w-[60px] text-green-600 font-bold">[{i.toString().padStart(2, '0')}]</span>
                        <span className="opacity-80 group-hover:opacity-100 select-all tracking-wider">{rk}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-green-900/40 text-xs font-mono border border-dashed border-green-900/30 rounded-xl min-h-[200px]">
              System Idle. Enter plaintext and click Encrypt.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
