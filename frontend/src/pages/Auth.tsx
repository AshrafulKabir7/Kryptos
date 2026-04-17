import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Lock, User, ArrowLeft, Eye, EyeOff, Fingerprint } from 'lucide-react';

export default function Auth() {
  const navigate = useNavigate();
  const location = useLocation();
  const isLogin = location.pathname === '/login';
  
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const endpoint = isLogin ? '/auth/login' : '/auth/register';
    
    try {
      const response = await fetch(`http://localhost:8000/api${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Authentication Failed");
      }

      if (isLogin) {
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('auth_user', data.user);
        navigate('/dashboard');
      } else {
        setSuccess('Profile generated. Redirecting to authentication...');
        setTimeout(() => navigate('/login'), 1200);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative font-sans flex flex-col items-center justify-center p-6 bg-[#070b09] overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <motion.div
          animate={{ scale: [1, 1.15, 1], rotate: [0, 90, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-green-500/10 blur-[150px] rounded-full mix-blend-screen"
        />
        <motion.div
          animate={{ scale: [1, 1.1, 1], x: [0, 50, 0] }}
          transition={{ duration: 14, repeat: Infinity, ease: "linear" }}
          className="absolute top-[20%] right-[10%] w-[200px] h-[200px] bg-emerald-500/10 blur-[100px] rounded-full mix-blend-screen"
        />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] mix-blend-overlay"></div>
        {/* Grid overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(34,197,94,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(34,197,94,0.03)_1px,transparent_1px)] bg-[size:60px_60px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_60%,transparent_100%)]"></div>
      </div>

      <div className="relative z-10 w-full max-w-md">
        
        <motion.button 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          whileHover={{ x: -5 }}
          onClick={() => navigate('/')}
          className="mb-8 flex items-center gap-2 text-slate-500 hover:text-green-400 transition-colors uppercase tracking-widest text-xs font-bold"
        >
          <ArrowLeft className="w-4 h-4" /> Return to Root
        </motion.button>

        <motion.div 
          initial={{ opacity: 0, y: 30, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, type: "spring", bounce: 0.2 }}
          className="glass-card p-10 flex flex-col items-center relative overflow-hidden"
        >
          {/* Animated border glow */}
          <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-transparent via-green-500/10 to-transparent opacity-50 pointer-events-none" />
          
          <motion.div 
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 0.5, delay: 0.2, type: "spring" }}
            className="w-16 h-16 rounded-2xl bg-green-500/10 border border-green-500/20 flex items-center justify-center shadow-[0_0_30px_rgba(34,197,94,0.2)] mb-6 relative"
          >
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
              className="absolute inset-[-2px] rounded-2xl border border-green-500/20 border-dashed"
            />
            <Fingerprint className="w-8 h-8 text-green-400" />
          </motion.div>

          <AnimatePresence mode="wait">
            <motion.div
              key={isLogin ? 'login' : 'signup'}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="text-center"
            >
              <h2 className="text-2xl font-black text-white tracking-widest uppercase mb-1">
                {isLogin ? 'Authentication' : 'Initialization'}
              </h2>
              <p className="text-slate-500 text-xs font-mono mb-8 text-center">
                {isLogin ? 'Enter credentials to access secure dashboard.' : 'Register new node profile on the network.'}
              </p>
            </motion.div>
          </AnimatePresence>

          {error && (
            <motion.div 
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className="w-full mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-mono text-center"
            >
              [!] {error}
            </motion.div>
          )}

          {success && (
            <motion.div 
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className="w-full mb-6 p-4 rounded-lg bg-green-500/10 border border-green-500/30 text-green-400 text-xs font-mono text-center"
            >
              ✓ {success}
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="w-full space-y-5">
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
              <label className="section-label flex items-center gap-2 mb-2"><User className="w-3 h-3" /> Identity Alias</label>
              <input 
                type="text" 
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-dark bg-[#0a0f0d] focus:shadow-[0_0_20px_rgba(34,197,94,0.15)] transition-shadow" 
                placeholder="system_admin"
              />
            </motion.div>
            
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }}>
              <label className="section-label flex items-center gap-2 mb-2"><Lock className="w-3 h-3" /> Master Passphrase</label>
              <div className="relative">
                <input 
                  type={showPassword ? "text" : "password"} 
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-dark bg-[#0a0f0d] pr-12 focus:shadow-[0_0_20px_rgba(34,197,94,0.15)] transition-shadow" 
                  placeholder="••••••••••••"
                />
                <button 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-green-400 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </motion.div>

            <motion.button 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              whileHover={{ scale: 1.02, boxShadow: "0 0 30px rgba(34,197,94,0.3)" }}
              whileTap={{ scale: 0.98 }}
              disabled={loading} 
              type="submit" 
              className="btn-primary w-full py-3.5 mt-4 text-sm disabled:opacity-50 flex items-center justify-center gap-2 relative overflow-hidden group"
            >
              <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.15),transparent)] -translate-x-[150%] group-hover:translate-x-[150%] transition-transform duration-700 ease-out" />
              {loading ? <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" /> : null}
              {isLogin ? 'Establish Secure Connection' : 'Generate Profile'}
            </motion.button>
          </form>

          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-8 text-xs font-mono text-slate-500 uppercase tracking-widest"
          >
            {isLogin ? (
              <p>Unknown Identity? <button onClick={() => navigate('/signup')} className="text-green-400 hover:text-green-300 ml-2 hover:underline underline-offset-4 transition-all">Initialize Here</button></p>
            ) : (
              <p>Already Initialized? <button onClick={() => navigate('/login')} className="text-green-400 hover:text-green-300 ml-2 hover:underline underline-offset-4 transition-all">Authenticate</button></p>
            )}
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
