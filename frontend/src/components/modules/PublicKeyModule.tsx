import { useState } from "react";
import { api } from "@/lib/api";
import { ShieldCheck, Server, KeySquare, Key, Lock, Unlock } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useFlow } from "@/context/FlowContext";
export function PublicKeyModule() {
  const [activeTab, setActiveTab] = useState<"rsa" | "ecc">("rsa");

  return (
    <div className="glass-card p-6 md:p-10 relative overflow-hidden">
      <div className="absolute top-[-50px] right-[-50px] w-64 h-64 bg-green-500/5 blur-[80px] rounded-full pointer-events-none" />

      <div className="mb-10 relative z-10 flex flex-col items-center text-center">
        <h2 className="text-2xl font-black uppercase tracking-widest text-white mb-3">
          Public Key <span className="gradient-text-neon">Cryptography</span>
        </h2>
        <p className="text-slate-500 text-xs font-mono max-w-xl leading-relaxed">
          Asymmetric algorithms. Public/Private keypairs to negotiate secure channels over insecure paths.
        </p>
      </div>

      <div className="flex gap-3 mb-8 relative z-10 justify-center">
        <button onClick={() => setActiveTab("rsa")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded border transition-all duration-300 text-xs font-bold uppercase tracking-wider ${activeTab === 'rsa' ? 'bg-[#0f1714] text-green-400 border-green-500/20 shadow-[0_0_20px_rgba(34,197,94,0.1)]' : 'bg-transparent text-slate-500 border-white/5 hover:bg-white/[0.02] hover:text-slate-300'}`}>
          RSA Engine
        </button>
        <button onClick={() => setActiveTab("ecc")}
          className={`flex items-center gap-2 px-5 py-2.5 rounded border transition-all duration-300 text-xs font-bold uppercase tracking-wider ${activeTab === 'ecc' ? 'bg-[#0f1714] text-green-400 border-green-500/20 shadow-[0_0_20px_rgba(34,197,94,0.1)]' : 'bg-transparent text-slate-500 border-white/5 hover:bg-white/[0.02] hover:text-slate-300'}`}>
          ECC / ECDH
        </button>
      </div>

      <div className="relative z-10 min-h-[400px]">
        <AnimatePresence mode="wait">
          {activeTab === "rsa" ? (
            <motion.div key="rsa" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 10 }} transition={{ duration: 0.2 }}>
              <RSAAlgorithm />
            </motion.div>
          ) : (
            <motion.div key="ecc" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 10 }} transition={{ duration: 0.2 }}>
              <ECCAlgorithm />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function RSAAlgorithm() {
  const [bits, setBits] = useState("512");
  const [keys, setKeys] = useState<any>(null);
  const [plaintext, setPlaintext] = useState("");
  const [ciphertext, setCiphertext] = useState("");
  const [decryptedText, setDecryptedText] = useState("");
  const { triggerFlow } = useFlow();

  const handleGenerate = async () => {
    triggerFlow("rsa_keygen", "encrypt");
    try {
      const res = await api.post(`/public/rsa/generate`, { bits: parseInt(bits) || 512 });
      setKeys(res.data);
      setCiphertext("");
      setDecryptedText("");
    } catch (err: any) {
      alert("Error: " + err);
    }
  };

  const handleEncrypt = async () => {
    if (!keys) return alert("Generate keys first!");
    triggerFlow("rsa", "encrypt");
    try {
      const res = await api.post(`/public/rsa/encrypt`, { 
        text: plaintext, n: keys.public_key.n, e: keys.public_key.e 
      });
      setCiphertext(res.data.ciphertext.toString());
    } catch (err: any) {
      alert("Encryption Error: " + err);
    }
  };

  const handleDecrypt = async () => {
    if (!keys || !ciphertext) return alert("Missing keys or ciphertext!");
    triggerFlow("rsa", "decrypt");
    try {
      const res = await api.post(`/public/rsa/decrypt`, { 
        ciphertext: ciphertext, n: keys.private_key.n, d: keys.private_key.d 
      });
      setDecryptedText(res.data.plaintext);
    } catch (err: any) {
      alert("Decryption Error: " + err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Step 1: Key Generation */}
      <div className="bg-[#0f1714] border border-green-500/20 p-6 rounded-xl shadow-[0_0_30px_rgba(34,197,94,0.03)]">
        <div className="section-label flex items-center gap-2"><Key className="w-3 h-3 text-green-500" /> Step 1: Generate Keys</div>
        <p className="text-[10px] text-slate-500 font-mono mb-4">Choose key size (e.g., 512, 1024 bits). Keys are randomly generated.</p>
        
        <div className="flex gap-4">
          <select value={bits} onChange={(e) => setBits(e.target.value)} className="input-dark w-48 bg-[#0a0f0d]">
            <option value="512">512 bits</option>
            <option value="1024">1024 bits</option>
            <option value="2048">2048 bits</option>
          </select>
          <button onClick={handleGenerate} className="btn-primary px-8">Generate Keys</button>
        </div>

        {keys && (
          <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} className="mt-5 space-y-3">
            {/* Public Key Output */}
            <div className="bg-black/40 p-4 rounded-lg border border-green-500/10">
              <div className="text-[9px] text-green-500 font-bold uppercase tracking-widest mb-2 flex items-center gap-1.5">
                <Lock className="w-3 h-3" /> Output: Public Key (n, e)
              </div>
              <div className="font-mono text-xs text-slate-300 break-all leading-relaxed">
                <span className="text-slate-500">n = </span>
                <span className="select-all cursor-pointer hover:text-white transition-colors">{keys.public_key.n}</span>
              </div>
              <div className="font-mono text-xs text-green-400 mt-1">
                <span className="text-slate-500">e = </span>{keys.public_key.e}
              </div>
            </div>
            {/* Private Key Output */}
            <div className="bg-green-500/5 p-4 rounded-lg border border-green-500/20">
              <div className="text-[9px] text-green-400 font-bold uppercase tracking-widest mb-2 flex items-center gap-1.5">
                <Unlock className="w-3 h-3" /> Output: Private Key (n, d)
              </div>
              <div className="font-mono text-xs text-slate-300 break-all leading-relaxed">
                <span className="text-slate-500">d = </span>
                <span className="select-all cursor-pointer hover:text-white transition-colors">{keys.private_key.d}</span>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Step 2: Encrypt */}
        <div className="bg-white/[0.01] border border-white/5 p-6 rounded-xl">
          <div className="section-label flex items-center gap-2"><ShieldCheck className="w-3 h-3 text-green-500" /> Step 2: Encrypt</div>
          <div className="section-label text-slate-600 !mb-3">Input: Plaintext String</div>
          <input placeholder="Enter your secret message..." value={plaintext} onChange={(e) => setPlaintext(e.target.value)} className="input-dark mb-4" />
          <button onClick={handleEncrypt} className="btn-primary w-full">Encrypt with Public Key</button>
          
          {ciphertext && (
            <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} className="mt-4">
              <div className="section-label text-green-500">Output: Ciphertext (Integer)</div>
              <div className="result-box text-green-300 text-xs min-h-[60px] break-all">{ciphertext}</div>
            </motion.div>
          )}
        </div>

        {/* Step 3: Decrypt */}
        <div className="bg-[#050807] border border-green-500/10 p-6 rounded-xl">
          <div className="section-label flex items-center gap-2"><Unlock className="w-3 h-3 text-amber-500" /> Step 3: Decrypt</div>
          <div className="section-label text-slate-600 !mb-3">Ciphertext (auto-filled or paste)</div>
          <textarea placeholder="Ciphertext integer..." value={ciphertext} onChange={(e) => setCiphertext(e.target.value)} 
            className="textarea-dark min-h-[80px] text-green-100 break-all mb-4" />
          <button onClick={handleDecrypt} className="bg-[#0d1210] border border-green-500/20 text-green-400 hover:bg-green-500/20 hover:text-white transition-all w-full flex items-center justify-center p-3 rounded-xl font-bold uppercase tracking-wider text-xs gap-2">
            <ShieldCheck className="w-4 h-4" /> Decrypt with Private Key
          </button>

          {decryptedText && (
            <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} className="mt-4 p-4 bg-green-500/10 border border-green-500/30 rounded-xl text-center">
              <div className="text-[9px] uppercase font-bold tracking-widest text-green-500 mb-1">Output: Decrypted Message</div>
              <div className="text-white font-medium tracking-wide text-lg">{decryptedText}</div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}

function ECCAlgorithm() {
  const [curve, setCurve] = useState("P-256");
  const [alice, setAlice] = useState<any>(null);
  const [bob, setBob] = useState<any>(null);
  const [shared, setShared] = useState<any>(null);
  const { triggerFlow } = useFlow();

  const handleGenerateAlice = async () => {
    try {
      const res = await api.post(`/public/ecc/generate`, { curve_name: curve });
      setAlice(res.data);
      setShared(null);
    } catch (err) { alert(err) }
  };

  const handleGenerateBob = async () => {
    try {
      const res = await api.post(`/public/ecc/generate`, { curve_name: curve });
      setBob(res.data);
      setShared(null);
    } catch (err) { alert(err) }
  };

  const handleComputeShared = async () => {
    if (!alice || !bob) return alert("Generate both Node A and Node B keys first!");
    triggerFlow("ecdh", "encrypt");
    try {
      const res = await api.post(`/public/ecc/ecdh`, { 
        curve_name: curve,
        private_key: alice.private_key,
        other_public_x: bob.public_key.x,
        other_public_y: bob.public_key.y,
      });
      setShared(res.data);
    } catch (err) { alert(err) }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Domain Parameters Selection */}
      <div className="bg-[#0f1714] border border-green-500/20 p-6 rounded-xl">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <div className="text-slate-300 font-bold uppercase tracking-widest text-xs flex items-center gap-2 mb-1">
              <Server className="w-4 h-4 text-green-500"/> Domain Parameters
            </div>
            <p className="text-[10px] text-slate-500 font-mono">Select curve to define (p, a, b, G, n)</p>
          </div>
          <select value={curve} onChange={(e) => { setCurve(e.target.value); setAlice(null); setBob(null); setShared(null); }}
            className="input-dark w-64 bg-[#0a0f0d] border-green-500/15 text-xs">
            <option value="Demo">Demo Educational Curve</option>
            <option value="secp256k1">secp256k1 (Bitcoin)</option>
            <option value="P-256">NIST P-256</option>
          </select>
        </div>

        {/* Show domain parameters when a key is generated */}
        {alice && alice.domain && (
          <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} className="mt-5 bg-black/30 p-4 rounded-lg border border-white/5">
            <div className="text-[9px] text-green-500 font-bold uppercase tracking-widest mb-3">Output: Domain Parameters (p, a, b, G, n)</div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 font-mono text-[10px]">
              {Object.entries(alice.domain).map(([key, val]) => (
                <div key={key} className="bg-white/[0.02] p-2 rounded border border-white/5 overflow-hidden">
                  <span className="text-slate-500 block mb-0.5 uppercase">{key}</span>
                  <span className="text-green-300 break-all text-[9px] leading-relaxed block max-h-[40px] overflow-auto">{String(val)}</span>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* Node A and Node B */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Node A (Alice) */}
        <div className="bg-[#0b100e] border border-green-500/10 p-6 rounded-xl">
          <h4 className="font-black text-slate-300 uppercase tracking-widest mb-4 flex items-center gap-2">
            <KeySquare className="w-4 h-4 text-green-500"/> Node A (Alice)
          </h4>
          <button onClick={handleGenerateAlice} className="btn-outline border-white/10 hover:border-green-500/50 w-full mb-5 py-2.5">Generate Key Pair</button>
          <div className="font-mono text-xs space-y-3">
            <div className="bg-black/30 p-3 rounded-lg border border-white/5">
              <div className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1">Output: Private Key (dₐ)</div>
              <div className="text-slate-300 break-all leading-relaxed">{alice ? alice.private_key : "—"}</div>
            </div>
            {alice && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-green-500/5 p-3 rounded-lg border border-green-500/20">
                <div className="text-[9px] text-green-500 font-bold uppercase tracking-widest mb-1">Output: Public Key Qₐ(x, y)</div>
                <div className="text-green-300 break-all leading-relaxed text-[10px]">
                  <span className="text-slate-500">x = </span>{alice.public_key.x}
                </div>
                <div className="text-green-300 break-all leading-relaxed text-[10px] mt-1">
                  <span className="text-slate-500">y = </span>{alice.public_key.y}
                </div>
              </motion.div>
            )}
          </div>
        </div>
        
        {/* Node B (Bob) */}
        <div className="bg-[#0b100e] border border-green-500/10 p-6 rounded-xl">
          <h4 className="font-black text-slate-300 uppercase tracking-widest mb-4 flex items-center gap-2">
            <KeySquare className="w-4 h-4 text-green-500"/> Node B (Bob)
          </h4>
          <button onClick={handleGenerateBob} className="btn-outline border-white/10 hover:border-green-500/50 w-full mb-5 py-2.5">Generate Key Pair</button>
          <div className="font-mono text-xs space-y-3">
            <div className="bg-black/30 p-3 rounded-lg border border-white/5">
              <div className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1">Output: Private Key (d_b)</div>
              <div className="text-slate-300 break-all leading-relaxed">{bob ? bob.private_key : "—"}</div>
            </div>
            {bob && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-green-500/5 p-3 rounded-lg border border-green-500/20">
                <div className="text-[9px] text-green-500 font-bold uppercase tracking-widest mb-1">Output: Public Key Q_b(x, y)</div>
                <div className="text-green-300 break-all leading-relaxed text-[10px]">
                  <span className="text-slate-500">x = </span>{bob.public_key.x}
                </div>
                <div className="text-green-300 break-all leading-relaxed text-[10px] mt-1">
                  <span className="text-slate-500">y = </span>{bob.public_key.y}
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>

      {/* ECDH Shared Key Computation */}
      <div className="flex flex-col items-center pt-4">
        <button onClick={handleComputeShared} 
          className="btn-primary w-full md:w-1/2 py-4 shadow-[0_0_30px_rgba(34,197,94,0.2)] text-xs uppercase">
          Compute ECDH Shared Key (a, b)
        </button>

        <AnimatePresence>
          {shared && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              className="mt-8 w-full bg-[#050807] p-6 border border-green-500/20 rounded-xl"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-2.5 h-2.5 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e] animate-pulse"></div>
                <h4 className="text-green-400 text-xs font-black tracking-widest uppercase">Output: ECDH Shared Key</h4>
              </div>
              <div className="font-mono text-xs break-all space-y-3">
                <div className="border-l-2 border-green-500 pl-4 py-1">
                  <span className="text-slate-500 uppercase text-[9px] tracking-widest block mb-1">Shared Secret (x-coordinate)</span>
                  <span className="text-green-300 text-sm leading-relaxed select-all">{shared.shared_key_x}</span>
                </div>
                <div className="border-l-2 border-green-500/40 pl-4 py-1">
                  <span className="text-slate-500 uppercase text-[9px] tracking-widest block mb-1">Shared Secret (y-coordinate)</span>
                  <span className="text-green-300 text-sm leading-relaxed select-all">{shared.shared_key_y}</span>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}





export function ECCAlgorithm() {
  const [activeSubTab, setActiveSubTab] = useState<"keygen" | "ecdh">("keygen");

  // State for Step 1
  const [a, setA] = useState("1");
  const [b, setB] = useState("1");
  const [p, setP] = useState("23");
  const [points, setPoints] = useState<any[]>([]);
  
  // State for Step 2
  const [gx, setGx] = useState("");
  const [gy, setGy] = useState("");
  const [orderN, setOrderN] = useState<string | null>(null);

  // State for Step 3 Keygen
  const [d, setD] = useState("");
  const [keyPair, setKeyPair] = useState<any>(null);

  // State for Step 2 ECDH
  const [privA, setPrivA] = useState("");
  const [privB, setPrivB] = useState("");
  const [ecdhResult, setEcdhResult] = useState<any>(null);

  // Logs/Output
  const [outputLog, setOutputLog] = useState<string[]>(["Complete steps to see output."]);

  const addLog = (msg: string) => setOutputLog(prev => [...prev, msg]);

  const handleFindPoints = async () => {
    try {
      const res = await api.post(`/public/ecc/points`, { 
        p: parseInt(p), a: parseInt(a), b: parseInt(b) 
      });
      setPoints(res.data.points);
      addLog(`Found ${res.data.points.length} points for curve y² = x³ + ${a}x + ${b} (mod ${p}).`);
    } catch (err: any) { alert("Error: " + (err.response?.data?.detail || err.message)); }
  };

  const handleSetGenerator = async () => {
    if (!gx || !gy) return alert("Please select a point or enter G.x and G.y");
    try {
      const res = await api.post(`/public/ecc/order`, { 
        p: parseInt(p), a: parseInt(a), b: parseInt(b), Gx: parseInt(gx), Gy: parseInt(gy)
      });
      setOrderN(res.data.n.toString());
      addLog(`Generator G = (${gx}, ${gy}) has Order n = ${res.data.n}.`);
    } catch (err: any) { alert("Error: " + (err.response?.data?.detail || err.message)); }
  };

  const handleGenerateKey = async () => {
    try {
      const res = await api.post(`/public/ecc/keypair`, { 
        p: parseInt(p), a: parseInt(a), b: parseInt(b), 
        Gx: parseInt(gx), Gy: parseInt(gy),
        n: orderN ? parseInt(orderN) : undefined,
        private_key: d ? parseInt(d) : undefined
      });
      setKeyPair(res.data);
      addLog(`Generated Key Pair. Private d = ${res.data.private_key}, Public Q = (${res.data.public_key.x}, ${res.data.public_key.y}).`);
    } catch (err: any) { alert("Error: " + (err.response?.data?.detail || err.message)); }
  };

  const handleRunECDH = async () => {
    if (!gx || !gy) return alert("Please set Generator G first!");
    try {
      // Auto-generate if blank, we can just pass some random if not provided, but backend requires ints.
      // So if blank, we will generate them locally to pass, or let backend do it. Backend ecdh endpoint needs priv_A and priv_B.
      // Let's generate random ones if blank.
      let finalPrivA = privA ? parseInt(privA) : Math.floor(Math.random() * (parseInt(orderN || "20") - 2)) + 2;
      let finalPrivB = privB ? parseInt(privB) : Math.floor(Math.random() * (parseInt(orderN || "20") - 2)) + 2;

      setPrivA(finalPrivA.toString());
      setPrivB(finalPrivB.toString());

      const res = await api.post(`/public/ecc/ecdh`, { 
        p: parseInt(p), a: parseInt(a), b: parseInt(b), 
        Gx: parseInt(gx), Gy: parseInt(gy),
        priv_A: finalPrivA, priv_B: finalPrivB
      });
      setEcdhResult(res.data);
      addLog(`ECDH Success! Shared Secret = (${res.data.shared_secret.x}, ${res.data.shared_secret.y}).`);
    } catch (err: any) { alert("Error: " + (err.response?.data?.detail || err.message)); }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Sub Tabs */}
      <div className="flex gap-2">
        <button onClick={() => setActiveSubTab("keygen")}
          className={`px-4 py-2 text-[10px] font-bold uppercase tracking-wider rounded ${activeSubTab === 'keygen' ? 'bg-green-500/20 text-green-400 border border-green-500/30' : 'bg-transparent border border-white/10 text-slate-400'}`}>
          KEY GENERATION
        </button>
        <button onClick={() => setActiveSubTab("ecdh")}
          className={`px-4 py-2 text-[10px] font-bold uppercase tracking-wider rounded ${activeSubTab === 'ecdh' ? 'bg-green-500/20 text-green-400 border border-green-500/30' : 'bg-transparent border border-white/10 text-slate-400'}`}>
          ECDH KEY EXCHANGE
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* LEFT COLUMN - STEPS */}
        <div className="space-y-4">
          
          {/* STEP 1 */}
          <div className="bg-[#0b100e] border border-green-500/10 p-5 rounded-xl">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <span className="text-xs text-green-500 font-bold uppercase tracking-widest">STEP 1 - DEFINE THE CURVE</span>
            </div>
            <p className="text-[10px] text-slate-400 font-mono mb-4">Enter parameters for y² = x³ + ax + b (mod p)</p>
            <div className="grid grid-cols-3 gap-3 mb-4">
              <div>
                <label className="text-[9px] text-slate-500 block mb-1">A</label>
                <input value={a} onChange={e => setA(e.target.value)} className="input-dark w-full text-xs py-1" />
              </div>
              <div>
                <label className="text-[9px] text-slate-500 block mb-1">B</label>
                <input value={b} onChange={e => setB(e.target.value)} className="input-dark w-full text-xs py-1" />
              </div>
              <div>
                <label className="text-[9px] text-slate-500 block mb-1">P (PRIME)</label>
                <input value={p} onChange={e => setP(e.target.value)} className="input-dark w-full text-xs py-1" />
              </div>
            </div>
            <div className="flex gap-2">
              <button onClick={handleFindPoints} className="btn-outline border-green-500/20 hover:border-green-500/50 text-[10px] py-1.5 px-3">FIND ALL POINTS</button>
            </div>
          </div>

          {/* STEP 2 */}
          <div className="bg-[#0b100e] border border-green-500/10 p-5 rounded-xl">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <span className="text-xs text-green-500 font-bold uppercase tracking-widest">STEP 2 - CHOOSE GENERATOR G</span>
            </div>
            <p className="text-[10px] text-slate-400 font-mono mb-4">Click a point in the output or enter coordinates.</p>
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label className="text-[9px] text-slate-500 block mb-1">G.X</label>
                <input value={gx} onChange={e => setGx(e.target.value)} placeholder="x coordinate" className="input-dark w-full text-xs py-1" />
              </div>
              <div>
                <label className="text-[9px] text-slate-500 block mb-1">G.Y</label>
                <input value={gy} onChange={e => setGy(e.target.value)} placeholder="y coordinate" className="input-dark w-full text-xs py-1" />
              </div>
            </div>
            <button onClick={handleSetGenerator} className="btn-outline border-green-500/20 hover:border-green-500/50 text-[10px] py-1.5 px-3">SET GENERATOR & COMPUTE ORDER</button>
            {orderN && <div className="mt-3 text-[10px] text-green-400 font-mono">Order n = {orderN}</div>}
          </div>

          {/* STEP 3 */}
          {activeSubTab === "keygen" ? (
            <div className="bg-[#0b100e] border border-green-500/10 p-5 rounded-xl">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2 h-2 rounded-full bg-green-500"></div>
                <span className="text-xs text-green-500 font-bold uppercase tracking-widest">STEP 3 - GENERATE KEY PAIR</span>
              </div>
              <p className="text-[10px] text-slate-400 font-mono mb-4">Choose private key d, or leave blank to auto-generate. Q = d×G.</p>
              <div className="mb-4">
                <label className="text-[9px] text-slate-500 block mb-1">PRIVATE KEY D (1 TO N-1)</label>
                <input value={d} onChange={e => setD(e.target.value)} placeholder="auto-generate if blank" className="input-dark w-full text-xs py-1" />
              </div>
              <div className="flex gap-2">
                <button onClick={handleGenerateKey} className="btn-outline border-green-500/20 hover:border-green-500/50 text-[10px] py-1.5 px-3">GENERATE KEY PAIR</button>
                <button onClick={() => setKeyPair(null)} className="btn-outline border-white/10 text-[10px] py-1.5 px-3">CLEAR</button>
              </div>
            </div>
          ) : (
            <div className="bg-[#0b100e] border border-green-500/10 p-5 rounded-xl">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2 h-2 rounded-full bg-green-500"></div>
                <span className="text-xs text-green-500 font-bold uppercase tracking-widest">STEP 3 - ALICE & BOB KEYS</span>
              </div>
              <div className="grid grid-cols-2 gap-3 mb-4">
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1">ALICE PRIVATE KEY A</label>
                  <input value={privA} onChange={e => setPrivA(e.target.value)} placeholder="auto" className="input-dark w-full text-xs py-1" />
                </div>
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1">BOB PRIVATE KEY B</label>
                  <input value={privB} onChange={e => setPrivB(e.target.value)} placeholder="auto" className="input-dark w-full text-xs py-1" />
                </div>
              </div>
              <button onClick={handleRunECDH} className="btn-outline border-green-500/20 hover:border-green-500/50 text-[10px] py-1.5 px-3 w-full mb-2">RUN ECDH EXCHANGE</button>
            </div>
          )}

        </div>

        {/* RIGHT COLUMN - OUTPUT */}
        <div className="bg-[#050807] border border-green-500/20 p-5 rounded-xl min-h-[400px] flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <span className="text-xs text-green-500 font-bold uppercase tracking-widest">OUTPUT</span>
            </div>
            <button onClick={() => { setOutputLog([]); setPoints([]); }} className="text-[9px] text-slate-500 hover:text-white">CLEAR OUTPUT</button>
          </div>
          
          <div className="flex-1 overflow-auto space-y-3 font-mono text-[10px]">
            {outputLog.map((log, i) => (
              <div key={i} className="text-slate-300 border-l-2 border-green-500/30 pl-2 py-0.5">{log}</div>
            ))}

            {points.length > 0 && (
              <div className="mt-4 p-3 bg-black/40 rounded border border-white/5">
                <div className="text-green-500 mb-2 font-bold uppercase">Points on Curve:</div>
                <div className="flex flex-wrap gap-1">
                  {points.map((pt, i) => (
                    <div key={i} onClick={() => { setGx(pt.x.toString()); setGy(pt.y.toString()); }}
                      className="px-2 py-1 bg-white/5 hover:bg-green-500/20 cursor-pointer rounded text-[9px] text-slate-300">
                      ({pt.x}, {pt.y})
                    </div>
                  ))}
                </div>
              </div>
            )}

            {keyPair && (
              <div className="mt-4 p-3 bg-green-500/10 rounded border border-green-500/20 space-y-2">
                <div className="text-green-400 font-bold uppercase">Generated Key Pair</div>
                <div>Private Key (d): <span className="text-white">{keyPair.private_key}</span></div>
                <div>Public Key (Q): <span className="text-white">({keyPair.public_key.x}, {keyPair.public_key.y})</span></div>
              </div>
            )}

            {ecdhResult && (
              <div className="mt-4 p-3 bg-green-500/10 rounded border border-green-500/20 space-y-2">
                <div className="text-green-400 font-bold uppercase">ECDH Complete</div>
                <div>Alice's Public Key: <span className="text-slate-300">({ecdhResult.alice_public.x}, {ecdhResult.alice_public.y})</span></div>
                <div>Bob's Public Key: <span className="text-slate-300">({ecdhResult.bob_public.x}, {ecdhResult.bob_public.y})</span></div>
                <div className="pt-2 mt-2 border-t border-green-500/20">
                  <span className="text-green-400 font-bold">SHARED SECRET:</span> <span className="text-white">({ecdhResult.shared_secret.x}, {ecdhResult.shared_secret.y})</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
