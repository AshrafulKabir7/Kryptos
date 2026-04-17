import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Key, Link as LinkIcon, RefreshCw, Hexagon, Power, Activity, Home, Shield, Cpu, BarChart3, Clock, Lock } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import { FlowProvider } from '@/context/FlowContext'
import { FlowPanel } from '@/components/FlowPanel'

// Modules
import { ClassicalModule } from '@/components/modules/ClassicalModule'
import { SymmetricModule } from '@/components/modules/SymmetricModule'
import { PublicKeyModule } from '@/components/modules/PublicKeyModule'

const navItems = [
  { id: 'classical', label: 'Classical', icon: RefreshCw, desc: 'Substitution & Transposition' },
  { id: 'symmetric', label: 'Symmetric', icon: LinkIcon, desc: 'AES-128 & DES Block Ciphers' },
  { id: 'public', label: 'Public Key', icon: Key, desc: 'RSA & Elliptic Curve ECDH' },
];

export default function Dashboard() {
  return (
    <FlowProvider>
      <DashboardInner />
    </FlowProvider>
  );
}

function DashboardInner() {
  const [activeModule, setActiveModule] = useState<string>("classical")
  const [currentTime, setCurrentTime] = useState(new Date())
  const navigate = useNavigate();
  const user = localStorage.getItem('auth_user') || 'ANONYMOUS';

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    navigate('/');
  };

  const activeNav = navItems.find(n => n.id === activeModule)!;

  return (
    <div className="min-h-screen relative font-sans bg-[#060a08]">
      {/* Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <motion.div
          animate={{ scale: [1, 1.08, 1], rotate: [0, 3, 0] }}
          transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
          className="absolute top-[-15%] left-[30%] w-[500px] h-[500px] bg-green-500/8 blur-[180px] rounded-full mix-blend-screen"
        />
        <motion.div
          animate={{ scale: [1, 1.05, 1], x: [0, 30, 0] }}
          transition={{ duration: 18, repeat: Infinity, ease: "linear" }}
          className="absolute bottom-[-10%] right-[5%] w-[400px] h-[400px] bg-emerald-500/5 blur-[140px] rounded-full mix-blend-screen"
        />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.02] mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-[linear-gradient(rgba(34,197,94,0.015)_1px,transparent_1px),linear-gradient(90deg,rgba(34,197,94,0.015)_1px,transparent_1px)] bg-[size:80px_80px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_40%,transparent_100%)]"></div>
      </div>

      {/* Layout: Sidebar + Main + Flow Panel */}
      <div className="relative z-10 flex min-h-screen">

        {/* Sidebar */}
        <motion.aside
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="w-[260px] min-h-screen border-r border-white/[0.04] bg-[#070b09]/80 backdrop-blur-xl flex flex-col p-5 sticky top-0 h-screen flex-shrink-0"
        >
          {/* Logo */}
          <div className="flex items-center gap-3 mb-10 group cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-9 h-9 rounded-lg bg-green-500/10 border border-green-500/20 flex items-center justify-center shadow-[0_0_15px_rgba(34,197,94,0.15)] group-hover:bg-green-500/20 transition-all">
              <Hexagon className="w-4 h-4 text-green-400" />
            </div>
            <div>
              <h1 className="text-sm font-black tracking-[0.25em] text-white uppercase">KRYPTOS</h1>
              <p className="text-[9px] text-slate-500 font-mono tracking-widest uppercase">Crypto Engine v1.0</p>
            </div>
          </div>

          {/* User Card */}
          <div className="mb-8 p-3 rounded-xl bg-white/[0.02] border border-white/[0.04]">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 flex items-center justify-center text-[#070b09] font-black text-sm">
                {user.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-bold text-white truncate">{user}</p>
                <p className="text-[10px] text-green-500 font-mono flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse inline-block"></span> Active
                </p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex-1">
            <p className="text-[9px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-4 px-2">Algorithms</p>
            <nav className="space-y-1.5">
              {navItems.map((item) => {
                const isActive = activeModule === item.id;
                return (
                  <motion.button
                    key={item.id}
                    whileTap={{ scale: 0.97 }}
                    onClick={() => setActiveModule(item.id)}
                    className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl text-left transition-all duration-300 relative group ${
                      isActive
                        ? 'bg-green-500/10 text-green-400'
                        : 'text-slate-400 hover:text-white hover:bg-white/[0.03]'
                    }`}
                  >
                    {isActive && (
                      <motion.div
                        layoutId="sidebar-active"
                        className="absolute left-0 top-[20%] bottom-[20%] w-[3px] bg-green-500 rounded-full shadow-[0_0_10px_rgba(34,197,94,0.5)]"
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      />
                    )}
                    <item.icon className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-green-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
                    <div className="min-w-0">
                      <p className="text-xs font-bold uppercase tracking-widest truncate">{item.label}</p>
                      <p className={`text-[9px] font-mono truncate ${isActive ? 'text-green-500/60' : 'text-slate-600'}`}>{item.desc}</p>
                    </div>
                  </motion.button>
                );
              })}
            </nav>
          </div>

          {/* Bottom Actions */}
          <div className="pt-6 border-t border-white/[0.04] space-y-2">
            <button
              onClick={() => navigate('/')}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-500 hover:text-white hover:bg-white/[0.03] transition-all text-xs"
            >
              <Home className="w-4 h-4" />
              <span className="font-bold uppercase tracking-widest">Home</span>
            </button>
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-500 hover:text-red-400 hover:bg-red-500/5 transition-all text-xs"
            >
              <Power className="w-4 h-4" />
              <span className="font-bold uppercase tracking-widest">Disconnect</span>
            </button>
          </div>
        </motion.aside>

        {/* Main Content */}
        <div className="flex-1 flex flex-col min-h-screen overflow-auto">

          {/* Top Bar */}
          <motion.header
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="sticky top-0 z-50 border-b border-white/[0.04] bg-[#060a08]/60 backdrop-blur-2xl"
          >
            <div className="flex items-center justify-between px-8 py-4">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <activeNav.icon className="w-5 h-5 text-green-400" />
                  <h2 className="text-lg font-black text-white uppercase tracking-widest">{activeNav.label}</h2>
                </div>
                <span className="text-[10px] font-mono text-slate-500 bg-white/[0.03] border border-white/[0.06] px-3 py-1 rounded-full uppercase tracking-widest hidden md:inline-flex items-center gap-1.5">
                  <Shield className="w-3 h-3 text-green-500/50" /> {activeNav.desc}
                </span>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-[10px] font-mono text-slate-500 bg-white/[0.02] border border-white/[0.04] px-3 py-1.5 rounded-lg">
                  <Clock className="w-3 h-3 text-green-500/50" />
                  {currentTime.toLocaleTimeString('en-US', { hour12: false })}
                </div>
                <div className="flex items-center gap-2 text-[10px] font-mono text-green-500/70 bg-green-500/5 border border-green-500/10 px-3 py-1.5 rounded-lg">
                  <Activity className="w-3 h-3 animate-pulse" />
                  ONLINE
                </div>
              </div>
            </div>
          </motion.header>

          {/* Stats Bar */}
          <div className="px-8 py-5">
            <div className="grid grid-cols-3 gap-4">
              <StatCard icon={<Cpu className="w-4 h-4" />} label="Algorithms" value="6" sub="Active Modules" />
              <StatCard icon={<Lock className="w-4 h-4" />} label="Key Sizes" value="128-4096" sub="Bit Range" />
              <StatCard icon={<BarChart3 className="w-4 h-4" />} label="Protocols" value="AES DES RSA ECC" sub="Supported Standards" />
            </div>
          </div>

          {/* Module Content */}
          <div className="flex-1 px-8 pb-10">
            <AnimatePresence mode="wait">
              {activeModule === "classical" && (
                <motion.div key="classical"
                  initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }}
                  transition={{ duration: 0.3, type: "spring", bounce: 0.15 }}
                >
                  <ClassicalModule />
                </motion.div>
              )}
              {activeModule === "symmetric" && (
                <motion.div key="symmetric"
                  initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }}
                  transition={{ duration: 0.3, type: "spring", bounce: 0.15 }}
                >
                  <SymmetricModule />
                </motion.div>
              )}
              {activeModule === "public" && (
                <motion.div key="public"
                  initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -12 }}
                  transition={{ duration: 0.3, type: "spring", bounce: 0.15 }}
                >
                  <PublicKeyModule />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Flow Panel (right side, appears on trigger) */}
        <FlowPanel />
      </div>
    </div>
  )
}

function StatCard({ icon, label, value, sub }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -2, borderColor: 'rgba(34,197,94,0.2)' }}
      className="bg-white/[0.015] border border-white/[0.04] rounded-xl p-4 flex items-center gap-4 group transition-all cursor-default"
    >
      <div className="w-10 h-10 rounded-lg bg-green-500/8 border border-green-500/15 flex items-center justify-center text-green-400 group-hover:scale-110 group-hover:bg-green-500/15 transition-all">
        {icon}
      </div>
      <div>
        <p className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">{label}</p>
        <p className="text-sm font-black text-white uppercase tracking-wider">{value}</p>
        <p className="text-[9px] text-slate-600 font-mono">{sub}</p>
      </div>
    </motion.div>
  );
}
