import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Hexagon, Zap, Server, ArrowRight, User, Terminal, Shield, Mail, Globe, Code2, Lock, KeyRound, Binary, Cpu, ArrowDown, Fingerprint, Layers, Hash, Network, Link, Code } from 'lucide-react';

const fadeUp = {
  initial: { opacity: 0, y: 30 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-60px" },
};

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen relative font-sans flex flex-col bg-[#060a08] overflow-hidden">
      {/* Dynamic Animated Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <motion.div animate={{ y: [0, -30, 0], x: [0, 20, 0], scale: [1, 1.05, 1] }} transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-[5%] left-[-5%] w-[400px] h-[400px] bg-green-500/10 blur-[150px] rounded-full mix-blend-screen" />
        <motion.div animate={{ y: [0, 20, 0], x: [0, -15, 0], scale: [1, 1.08, 1] }} transition={{ duration: 15, repeat: Infinity, ease: "easeInOut", delay: 2 }}
          className="absolute bottom-[10%] right-[-5%] w-[500px] h-[500px] bg-emerald-500/8 blur-[180px] rounded-full mix-blend-screen" />
        <motion.div animate={{ scale: [1, 1.1, 1] }} transition={{ duration: 18, repeat: Infinity, ease: "easeInOut", delay: 4 }}
          className="absolute top-[50%] left-[40%] w-[250px] h-[250px] bg-green-400/5 blur-[120px] rounded-full mix-blend-screen" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-[linear-gradient(rgba(34,197,94,0.015)_1px,transparent_1px),linear-gradient(90deg,rgba(34,197,94,0.015)_1px,transparent_1px)] bg-[size:80px_80px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_40%,transparent_100%)]"></div>
      </div>

      <div className="relative z-10 flex flex-col">
        
        {/* ═══════════════ NAVIGATION ═══════════════ */}
        <motion.header initial={{ y: -20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.8 }}
          className="w-full pt-6 pb-4 sticky top-0 z-50 bg-[#060a08]/60 backdrop-blur-2xl border-b border-white/[0.03]">
          <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
            <motion.div whileHover={{ scale: 1.03 }} className="flex items-center gap-3 cursor-pointer">
              <div className="w-9 h-9 rounded-lg bg-green-500/10 border border-green-500/20 flex items-center justify-center shadow-[0_0_15px_rgba(34,197,94,0.15)] relative overflow-hidden">
                <Hexagon className="w-4 h-4 text-green-400 relative z-10" />
              </div>
              <h1 className="text-lg font-black tracking-[0.2em] text-white uppercase">
                KRYPTOS<span className="text-white/15 px-1.5 font-light">/</span><span className="text-green-400">ENGINE</span>
              </h1>
            </motion.div>

            <nav className="hidden md:flex items-center gap-8 text-[11px] font-bold uppercase tracking-[0.15em] text-slate-400">
              <a href="#features" className="hover:text-green-400 transition-colors">Features</a>
              <a href="#algorithms" className="hover:text-green-400 transition-colors">Algorithms</a>
              <a href="#how-it-works" className="hover:text-green-400 transition-colors">How It Works</a>
              <a href="#team" className="hover:text-green-400 transition-colors">Team</a>
            </nav>
            
            <div className="flex gap-3">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/login')} 
                className="px-5 py-2 rounded-lg text-xs font-bold text-slate-300 hover:text-white border border-white/[0.06] hover:border-white/15 transition-all">
                Log In
              </motion.button>
              <motion.button whileHover={{ scale: 1.05, boxShadow: "0 0 25px rgba(34,197,94,0.3)" }} whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/signup')} 
                className="btn-primary flex items-center gap-2 text-xs py-2 px-5 group relative overflow-hidden">
                <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.15),transparent)] -translate-x-[150%] group-hover:translate-x-[150%] transition-transform duration-700" />
                Sign Up <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </motion.button>
            </div>
          </div>
        </motion.header>

        {/* ═══════════════ HERO ═══════════════ */}
        <section className="flex flex-col items-center px-6 pt-24 pb-16 text-center">
          <motion.div {...fadeUp} transition={{ duration: 0.5, delay: 0.1 }}
            className="mb-8 flex border border-green-500/20 bg-green-500/5 rounded-full px-4 py-1.5 shadow-inner hover:scale-105 transition-transform cursor-pointer">
            <span className="text-[10px] font-mono text-green-400 tracking-[0.2em] uppercase flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_#22c55e] animate-pulse inline-block"></span>
              CSE 721 — Applied Cryptography Project
            </span>
          </motion.div>

          <div className="overflow-hidden">
            <motion.h2 initial={{ opacity: 0, y: 80 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, type: "spring", bounce: 0.15 }}
              className="text-5xl md:text-7xl lg:text-8xl font-black text-white leading-[0.95] tracking-wide uppercase max-w-5xl">
              A Universal<br />Cryptographic<br />
              <span className="gradient-text-neon">Compiler Engine</span>
            </motion.h2>
          </div>
          
          <motion.p {...fadeUp} transition={{ duration: 0.6, delay: 0.3 }}
            className="text-slate-400 mt-10 max-w-2xl text-sm md:text-base leading-relaxed">
            Kryptos is an interactive web-based cryptographic workbench. Input any plaintext message and watch it transform in real-time through classical ciphers, symmetric block encryption, or public-key algorithms — complete with step-by-step pipeline visualizations.
          </motion.p>
          
          <motion.div {...fadeUp} transition={{ duration: 0.5, delay: 0.5 }} className="flex flex-col sm:flex-row gap-4 mt-12">
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/signup')} 
              className="btn-primary px-10 py-4 text-sm flex items-center gap-3 shadow-[0_0_40px_rgba(34,197,94,0.2)] relative overflow-hidden group">
              <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.08)_50%,transparent_75%)] bg-[length:250%_250%] bg-no-repeat group-hover:bg-[position:200%_0] transition-[background-position] duration-700" />
              Get Started Free <Terminal className="w-4 h-4" />
            </motion.button>
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              onClick={() => { document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' }) }}
              className="btn-outline px-10 py-4 text-sm flex items-center gap-3">
              See How It Works <ArrowDown className="w-4 h-4" />
            </motion.button>
          </motion.div>

          {/* Scroll indicator */}
          <motion.div animate={{ y: [0, 8, 0] }} transition={{ duration: 2, repeat: Infinity }} className="mt-20 text-slate-600">
            <ArrowDown className="w-5 h-5" />
          </motion.div>
        </section>

        {/* ═══════════════ INTERACTIVE DEMO PREVIEW ═══════════════ */}
        <section className="w-full max-w-5xl mx-auto px-6 pb-24">
          <motion.div {...fadeUp} transition={{ duration: 0.7 }}
            whileHover={{ y: -4, boxShadow: "0 30px 60px -15px rgba(34,197,94,0.12)" }}
            className="glass-card relative rounded-2xl overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-green-500/10 to-transparent opacity-0 group-hover:opacity-100 -translate-x-[100%] group-hover:translate-x-[100%] transition-all duration-1500 pointer-events-none" />
            <div className="bg-[#050807] border-b border-green-500/10 p-3 flex items-center justify-between relative z-10">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-slate-700/50 hover:bg-red-400 transition-colors"></div>
                <div className="w-3 h-3 rounded-full bg-slate-700/50 hover:bg-yellow-400 transition-colors"></div>
                <div className="w-3 h-3 rounded-full bg-slate-700/50 hover:bg-green-400 transition-colors"></div>
              </div>
              <div className="text-[10px] text-slate-400 font-mono flex items-center gap-2"><Code2 className="w-3 h-3 text-green-500"/> AES-128 Symmetric Compilation</div>
              <div className="w-12"></div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-green-500/10 text-left relative z-10">
              <div className="bg-[#0b100e] p-8 relative overflow-hidden min-h-[260px]">
                <span className="absolute top-4 right-4 text-[9px] text-slate-500 font-black uppercase tracking-[0.15em] bg-white/5 px-2 py-1 rounded border border-white/10">Input</span>
                <div className="mt-8 font-mono text-xs text-slate-300 space-y-5">
                  <motion.p initial={{ opacity: 0 }} animate={{ opacity: 0.5 }} transition={{ delay: 0.5 }}>~ Target payload injection initiated...</motion.p>
                  <motion.p initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 1.2 }} className="text-white">&gt; <strong>We strike at dawn. The package is ready.</strong></motion.p>
                  <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.8 }} className="text-green-500 pt-4 flex items-center gap-2 animate-pulse"><Terminal className="w-3 h-3"/> Compiling via AES-128...</motion.p>
                </div>
                <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.015)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:30px_30px] pointer-events-none [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_10%,transparent_100%)]"></div>
              </div>
              <div className="bg-[#050807] p-8 relative overflow-hidden min-h-[260px]">
                <span className="absolute top-4 right-4 text-[9px] text-green-400 font-black uppercase tracking-[0.15em] bg-green-500/10 border border-green-500/20 px-2 py-1 rounded shadow-[0_0_10px_rgba(34,197,94,0.15)]">Output</span>
                <div className="mt-8 font-mono text-xs space-y-4 relative z-10">
                  <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.4 }} className="text-green-400 break-all select-all font-bold tracking-wider leading-relaxed">E2A4B7D9C1F84300A529B9F1 01A24CD39B7C19AF3E7D3F9A</motion.p>
                  <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.8 }} className="text-slate-600 text-[10px]">Master Secret: [REDACTED]</motion.p>
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 3.2 }} className="mt-4 border-l-2 border-green-500/30 pl-3">
                    <p className="text-[9px] text-slate-500 mb-2 uppercase tracking-widest">Round Keys Generated</p>
                    <p className="text-slate-400/60 break-all mb-1">[00] 2B7E151628AED2A6</p>
                    <p className="text-slate-400/60 break-all">[01] A0FAFE1788542CB1</p>
                  </motion.div>
                </div>
              </div>
            </div>
          </motion.div>
        </section>

        {/* ═══════════════ FEATURES ═══════════════ */}
        <section id="features" className="w-full max-w-7xl mx-auto px-6 py-24 border-t border-white/[0.03]">
          <motion.div {...fadeUp} className="text-center mb-16">
            <p className="text-[10px] font-bold text-green-500 uppercase tracking-[0.3em] mb-4">Core Capabilities</p>
            <h3 className="text-3xl md:text-4xl font-black text-white uppercase tracking-widest">
              Why <span className="gradient-text-neon">Kryptos</span>
            </h3>
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FeatureCard delay={0} icon={<Shield className="w-5 h-5" />} title="Real-Time Pipeline" 
              desc="Watch every stage of encryption unfold live — from plaintext injection through key expansion to final ciphertext generation." />
            <FeatureCard delay={0.15} icon={<Zap className="w-5 h-5" />} title="Six Algorithms" 
              desc="Substitution, Transposition, AES-128, DES, RSA, and Elliptic Curve ECDH — all in one unified interface." />
            <FeatureCard delay={0.3} icon={<Server className="w-5 h-5" />} title="Python Backend" 
              desc="Every algorithm is implemented from scratch in Python with a FastAPI layer — no external crypto libraries used." />
          </div>
        </section>

        {/* ═══════════════ ALGORITHM SHOWCASE ═══════════════ */}
        <section id="algorithms" className="w-full max-w-7xl mx-auto px-6 py-24 border-t border-white/[0.03]">
          <motion.div {...fadeUp} className="text-center mb-16">
            <p className="text-[10px] font-bold text-green-500 uppercase tracking-[0.3em] mb-4">Algorithm Library</p>
            <h3 className="text-3xl md:text-4xl font-black text-white uppercase tracking-widest">
              Supported <span className="gradient-text-neon">Protocols</span>
            </h3>
            <p className="text-slate-500 text-sm font-mono mt-4 max-w-xl mx-auto">Three families of cryptographic algorithms, each with dedicated tooling and visual feedback.</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <AlgorithmCard 
              delay={0}
              category="Classical"
              icon={<Hash className="w-5 h-5" />}
              algorithms={["Substitution Cipher", "Double Transposition"]}
              color="emerald"
              desc="Historical ciphers using character mapping and grid-based column permutations."
              keySize="26-char / keyword"
            />
            <AlgorithmCard 
              delay={0.15}
              category="Symmetric"
              icon={<Lock className="w-5 h-5" />}
              algorithms={["AES-128 (Rijndael)", "DES (Feistel)"]}
              color="green"
              desc="Modern block ciphers with auto-generated keys, round-key expansion, and S-Box transformations."
              keySize="128-bit / 64-bit"
            />
            <AlgorithmCard 
              delay={0.3}
              category="Public Key"
              icon={<Network className="w-5 h-5" />}
              algorithms={["RSA (up to 4096-bit)", "ECDH (P-256, secp256k1)"]}
              color="lime"
              desc="Asymmetric cryptography with prime factorization, modular exponentiation, and elliptic curve point multiplication."
              keySize="512–4096 bit / 256-bit"
            />
          </div>
        </section>

        {/* ═══════════════ HOW IT WORKS ═══════════════ */}
        <section id="how-it-works" className="w-full max-w-5xl mx-auto px-6 py-24 border-t border-white/[0.03]">
          <motion.div {...fadeUp} className="text-center mb-20">
            <p className="text-[10px] font-bold text-green-500 uppercase tracking-[0.3em] mb-4">Workflow</p>
            <h3 className="text-3xl md:text-4xl font-black text-white uppercase tracking-widest">
              How It <span className="gradient-text-neon">Works</span>
            </h3>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <StepCard step={1} icon={<Fingerprint />} title="Sign Up" desc="Create an account in seconds. Your session is secured locally." delay={0} />
            <StepCard step={2} icon={<Layers />} title="Choose Algorithm" desc="Pick from 6 algorithms across Classical, Symmetric, and Public Key families." delay={0.1} />
            <StepCard step={3} icon={<Terminal />} title="Enter Plaintext" desc="Type or paste your message. Keys are auto-generated or manually configured." delay={0.2} />
            <StepCard step={4} icon={<Binary />} title="View Results" desc="See ciphertext, round keys, and a live animated flow diagram of the process." delay={0.3} />
          </div>
        </section>

        {/* ═══════════════ STATS ═══════════════ */}
        <section className="w-full max-w-5xl mx-auto px-6 py-20 border-t border-white/[0.03]">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <StatBlock value="6" label="Algorithms" />
            <StatBlock value="3" label="Cipher Families" />
            <StatBlock value="4096" label="Max Key Bits" />
            <StatBlock value="100%" label="Python Built" />
          </div>
        </section>

        {/* ═══════════════ TECH STACK ═══════════════ */}
        <section className="w-full max-w-5xl mx-auto px-6 py-24 border-t border-white/[0.03]">
          <motion.div {...fadeUp} className="text-center mb-12">
            <p className="text-[10px] font-bold text-green-500 uppercase tracking-[0.3em] mb-4">Under The Hood</p>
            <h3 className="text-3xl font-black text-white uppercase tracking-widest">
              Tech <span className="gradient-text-neon">Stack</span>
            </h3>
          </motion.div>
          <motion.div {...fadeUp} className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { name: "React + TypeScript", desc: "Frontend Framework" },
              { name: "Tailwind CSS", desc: "Styling System" },
              { name: "Framer Motion", desc: "Animations" },
              { name: "FastAPI + Python", desc: "Backend Engine" },
            ].map((tech, i) => (
              <motion.div key={i} whileHover={{ y: -3, borderColor: 'rgba(34,197,94,0.3)' }}
                className="bg-white/[0.015] border border-white/[0.04] rounded-xl p-5 text-center transition-all">
                <p className="text-sm font-black text-white uppercase tracking-wider mb-1">{tech.name}</p>
                <p className="text-[10px] text-slate-500 font-mono uppercase tracking-widest">{tech.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </section>

        {/* ═══════════════ CREATORS ═══════════════ */}
        <section id="team" className="w-full max-w-5xl mx-auto px-6 py-24 border-t border-white/[0.03]">
          <motion.div {...fadeUp} className="text-center mb-16">
            <p className="text-[10px] font-bold text-green-500 uppercase tracking-[0.3em] mb-4">The Team</p>
            <h3 className="text-3xl md:text-4xl font-black text-white uppercase tracking-widest">
              Core <span className="gradient-text-neon">Maintainers</span>
            </h3>
            <p className="text-slate-500 font-mono text-xs mt-4 uppercase tracking-widest">
              The engineers behind the Kryptos Engine.
            </p>
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl mx-auto">
            <CreatorCard name="Farhan Faruk" role="Security Architect" icon={<Shield className="w-7 h-7 text-green-400 relative z-10 group-hover:scale-110 transition-transform" />} delay={0} />
            <CreatorCard name="Ashraful Kabir Alif" role="Lead Protocol Dev" icon={<Code2 className="w-7 h-7 text-green-400 relative z-10 group-hover:scale-110 transition-transform" />} delay={0.15} />
          </div>
        </section>

        {/* ═══════════════ CTA ═══════════════ */}
        <section className="w-full max-w-4xl mx-auto px-6 py-24">
          <motion.div {...fadeUp}
            className="glass-card p-12 md:p-16 text-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-transparent pointer-events-none" />
            <Cpu className="w-10 h-10 text-green-500/30 mx-auto mb-6" />
            <h3 className="text-3xl md:text-4xl font-black text-white uppercase tracking-widest mb-4 relative z-10">
              Ready to <span className="gradient-text-neon">Compile</span>?
            </h3>
            <p className="text-slate-400 text-sm max-w-lg mx-auto mb-10 relative z-10">
              Create a free account and start encrypting, decrypting, and generating keys across all six supported algorithms.
            </p>
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/signup')} 
              className="btn-primary px-12 py-4 text-base flex items-center gap-3 mx-auto shadow-[0_0_50px_rgba(34,197,94,0.25)] relative overflow-hidden group">
              <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.12),transparent)] -translate-x-[150%] group-hover:translate-x-[150%] transition-transform duration-700" />
              Launch Dashboard <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </motion.button>
          </motion.div>
        </section>

        {/* ═══════════════ FOOTER ═══════════════ */}
        <footer className="w-full border-t border-white/[0.03] bg-[#050807]">
          <div className="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <Hexagon className="w-5 h-5 text-green-500/40" />
              <span className="text-xs font-bold tracking-[0.15em] text-slate-500 uppercase">KRYPTOS © 2026 — CSE 721 Project</span>
            </div>
            <div className="flex gap-6 text-[10px] font-mono text-slate-500 uppercase tracking-[0.15em]">
              <span className="hover:text-green-400 transition-colors cursor-pointer hover:underline underline-offset-4">Documentation</span>
              <span className="hover:text-green-400 transition-colors cursor-pointer hover:underline underline-offset-4">Privacy</span>
              <span className="hover:text-green-400 transition-colors cursor-pointer flex items-center gap-1.5 hover:underline underline-offset-4"><Mail className="w-3 h-3"/> Contact</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

/* ═══════════════ SUB-COMPONENTS ═══════════════ */

function FeatureCard({ icon, title, desc, delay }: any) {
  return (
    <motion.div {...fadeUp} transition={{ duration: 0.5, delay }}
      whileHover={{ y: -6 }}
      className="glass-card p-8 relative overflow-hidden group border-white/[0.03] hover:border-green-500/20 transition-all duration-500">
      <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="absolute top-0 right-0 p-6 opacity-[0.02] group-hover:opacity-[0.06] transition-opacity duration-500">
        <div className="w-20 h-20 text-green-500 scale-[3] origin-top-right group-hover:rotate-12 transition-transform duration-700">{icon}</div>
      </div>
      <div className="w-11 h-11 rounded-xl bg-green-500/10 border border-green-500/20 flex items-center justify-center text-green-400 mb-5 group-hover:scale-110 group-hover:bg-green-500/15 group-hover:shadow-[0_0_15px_rgba(34,197,94,0.25)] transition-all duration-300 relative z-10">
        {icon}
      </div>
      <h4 className="text-base font-bold tracking-[0.12em] uppercase text-white mb-2 relative z-10">{title}</h4>
      <p className="text-xs text-slate-400 leading-relaxed relative z-10">{desc}</p>
    </motion.div>
  );
}

function AlgorithmCard({ category, icon, algorithms, desc, keySize, delay }: any) {
  return (
    <motion.div {...fadeUp} transition={{ duration: 0.5, delay }}
      whileHover={{ y: -6 }}
      className="glass-card p-8 relative overflow-hidden group border-white/[0.03] hover:border-green-500/20 transition-all duration-500">
      <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="flex items-center gap-3 mb-5 relative z-10">
        <div className="w-10 h-10 rounded-lg bg-green-500/10 border border-green-500/20 flex items-center justify-center text-green-400 group-hover:scale-110 transition-transform">{icon}</div>
        <h4 className="text-lg font-black tracking-[0.12em] uppercase text-white">{category}</h4>
      </div>
      <p className="text-xs text-slate-400 leading-relaxed mb-5 relative z-10">{desc}</p>
      <div className="space-y-2 mb-5 relative z-10">
        {algorithms.map((algo: string, i: number) => (
          <div key={i} className="flex items-center gap-2 text-xs font-mono text-slate-300">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500/60"></span> {algo}
          </div>
        ))}
      </div>
      <div className="relative z-10 text-[9px] font-mono text-slate-500 uppercase tracking-[0.15em] bg-white/[0.03] border border-white/[0.04] px-3 py-1.5 rounded-lg inline-block">
        <KeyRound className="w-3 h-3 inline mr-1.5 -mt-0.5 text-green-500/50" />Key: {keySize}
      </div>
    </motion.div>
  );
}

function StepCard({ step, icon, title, desc, delay }: any) {
  return (
    <motion.div {...fadeUp} transition={{ duration: 0.5, delay }}
      className="text-center relative group">
      <div className="w-14 h-14 rounded-2xl bg-green-500/10 border border-green-500/20 flex items-center justify-center text-green-400 mx-auto mb-5 group-hover:scale-110 group-hover:shadow-[0_0_20px_rgba(34,197,94,0.2)] transition-all">
        {icon}
      </div>
      <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-2 text-[9px] font-black text-green-500/40 tracking-[0.3em]">0{step}</div>
      <h4 className="text-sm font-bold tracking-[0.12em] uppercase text-white mb-2">{title}</h4>
      <p className="text-[11px] text-slate-500 leading-relaxed">{desc}</p>
    </motion.div>
  );
}

function StatBlock({ value, label }: any) {
  return (
    <motion.div {...fadeUp} className="text-center py-4">
      <p className="text-4xl md:text-5xl font-black gradient-text-neon tracking-wider">{value}</p>
      <p className="text-[10px] text-slate-500 uppercase tracking-[0.2em] font-bold mt-2">{label}</p>
    </motion.div>
  );
}

function CreatorCard({ name, role, delay, icon }: any) {
  return (
    <motion.div {...fadeUp} transition={{ duration: 0.5, delay }}
      whileHover={{ y: -4, boxShadow: "0 20px 40px -10px rgba(34,197,94,0.12)" }}
      className="glass-card p-6 flex items-center gap-5 group border-white/[0.03] hover:border-green-500/20 transition-all duration-300">
      <div className="w-16 h-16 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 p-[2px] shadow-[0_0_15px_rgba(34,197,94,0.15)] flex-shrink-0">
        <div className="w-full h-full bg-[#070b09] rounded-full flex items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 bg-green-500/10 group-hover:bg-green-500/25 transition-colors duration-500"></div>
          {icon || <User className="w-7 h-7 text-green-400 relative z-10 group-hover:scale-110 transition-transform" />}
        </div>
      </div>
      <div className="flex-1 min-w-0">
        <h4 className="text-base font-bold text-white tracking-[0.1em] uppercase group-hover:text-green-300 transition-colors truncate">{name}</h4>
        <p className="text-[10px] font-mono text-green-500 uppercase flex items-center gap-1.5 mt-0.5">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse inline-block"></span> {role}
        </p>
        <div className="flex gap-2 mt-3">
          <motion.span whileHover={{ scale: 1.2 }} className="w-7 h-7 rounded-full bg-white/5 flex items-center justify-center text-slate-400 hover:text-green-400 hover:bg-green-500/15 transition-all cursor-pointer"><Code className="w-3 h-3"/></motion.span>
          <motion.span whileHover={{ scale: 1.2 }} className="w-7 h-7 rounded-full bg-white/5 flex items-center justify-center text-slate-400 hover:text-green-400 hover:bg-green-500/15 transition-all cursor-pointer"><Link className="w-3 h-3"/></motion.span>
          <motion.span whileHover={{ scale: 1.2 }} className="w-7 h-7 rounded-full bg-white/5 flex items-center justify-center text-slate-400 hover:text-green-400 hover:bg-green-500/15 transition-all cursor-pointer"><Globe className="w-3 h-3"/></motion.span>
        </div>
      </div>
    </motion.div>
  );
}
