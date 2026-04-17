import { motion, AnimatePresence } from 'framer-motion';
import { useFlow } from '@/context/FlowContext';
import { ArrowDown, CheckCircle2, Circle, Loader2, X, Lock, Unlock } from 'lucide-react';

export function FlowPanel() {
  const { flow, clearFlow } = useFlow();

  return (
    <AnimatePresence>
      {flow.active && (
        <motion.div
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: 300, opacity: 1 }}
          exit={{ width: 0, opacity: 0 }}
          transition={{ type: "spring", stiffness: 200, damping: 30 }}
          className="h-screen sticky top-0 border-l border-white/[0.04] bg-[#070b09]/90 backdrop-blur-xl overflow-hidden flex flex-col"
        >
          <div className="p-5 flex-1 overflow-auto min-w-[300px]">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2">
                {flow.direction === 'encrypt' ? (
                  <Lock className="w-4 h-4 text-green-400" />
                ) : (
                  <Unlock className="w-4 h-4 text-amber-400" />
                )}
                <h3 className="text-xs font-black text-white uppercase tracking-widest">
                  Flow
                </h3>
              </div>
              <button
                onClick={clearFlow}
                className="w-6 h-6 rounded-md bg-white/5 hover:bg-white/10 flex items-center justify-center text-slate-500 hover:text-white transition-all"
              >
                <X className="w-3 h-3" />
              </button>
            </div>

            {/* Algorithm Badge */}
            <div className={`mb-6 p-3 rounded-lg border text-center ${
              flow.direction === 'encrypt'
                ? 'bg-green-500/5 border-green-500/20'
                : 'bg-amber-500/5 border-amber-500/20'
            }`}>
              <p className={`text-[10px] font-black uppercase tracking-[0.2em] ${
                flow.direction === 'encrypt' ? 'text-green-400' : 'text-amber-400'
              }`}>
                {flow.title}
              </p>
            </div>

            {/* Flow Steps */}
            <div className="relative">
              {flow.steps.map((step, i) => (
                <div key={i}>
                  <FlowStepNode step={step} index={i} isLast={i === flow.steps.length - 1} direction={flow.direction} />
                  {i < flow.steps.length - 1 && (
                    <FlowConnector status={step.status} direction={flow.direction} />
                  )}
                </div>
              ))}
            </div>

            {/* Completion Message */}
            <AnimatePresence>
              {flow.steps.every(s => s.status === 'done') && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ delay: 0.3, type: "spring" }}
                  className={`mt-6 p-4 rounded-xl border text-center ${
                    flow.direction === 'encrypt'
                      ? 'bg-green-500/10 border-green-500/20'
                      : 'bg-amber-500/10 border-amber-500/20'
                  }`}
                >
                  <CheckCircle2 className={`w-6 h-6 mx-auto mb-2 ${
                    flow.direction === 'encrypt' ? 'text-green-400' : 'text-amber-400'
                  }`} />
                  <p className="text-[10px] font-bold uppercase tracking-widest text-white">
                    Pipeline Complete
                  </p>
                  <p className="text-[9px] text-slate-500 mt-1 font-mono">
                    All {flow.steps.length} stages executed
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function FlowStepNode({ step, index, direction }: { step: any; index: number; isLast?: boolean; direction: string }) {
  const colorClass = direction === 'encrypt' ? 'green' : 'amber';

  return (
    <motion.div
      initial={{ opacity: 0, x: 10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      className={`flex items-start gap-3 p-3 rounded-lg transition-all duration-300 ${
        step.status === 'active'
          ? `bg-${colorClass}-500/10 border border-${colorClass}-500/20 shadow-[0_0_15px_rgba(34,197,94,0.1)]`
          : step.status === 'done'
          ? 'bg-white/[0.01]'
          : 'opacity-40'
      }`}
    >
      {/* Icon */}
      <div className="mt-0.5 flex-shrink-0">
        {step.status === 'done' ? (
          <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", bounce: 0.5 }}>
            <CheckCircle2 className={`w-4 h-4 ${direction === 'encrypt' ? 'text-green-500' : 'text-amber-500'}`} />
          </motion.div>
        ) : step.status === 'active' ? (
          <Loader2 className={`w-4 h-4 animate-spin ${direction === 'encrypt' ? 'text-green-400' : 'text-amber-400'}`} />
        ) : (
          <Circle className="w-4 h-4 text-slate-600" />
        )}
      </div>

      {/* Content */}
      <div className="min-w-0">
        <p className={`text-[11px] font-bold uppercase tracking-widest ${
          step.status === 'active'
            ? 'text-white'
            : step.status === 'done'
            ? 'text-slate-300'
            : 'text-slate-500'
        }`}>
          {step.label}
        </p>
        {step.detail && (
          <p className={`text-[9px] font-mono mt-0.5 ${
            step.status === 'active'
              ? direction === 'encrypt' ? 'text-green-400/70' : 'text-amber-400/70'
              : 'text-slate-600'
          }`}>
            {step.detail}
          </p>
        )}
      </div>
    </motion.div>
  );
}

function FlowConnector({ status, direction }: { status: string; direction: string }) {
  return (
    <div className="flex items-center justify-center py-1">
      <div className="flex flex-col items-center gap-0.5">
        <div className={`w-px h-3 ${
          status === 'done'
            ? direction === 'encrypt' ? 'bg-green-500/40' : 'bg-amber-500/40'
            : 'bg-white/10'
        }`} />
        <ArrowDown className={`w-2.5 h-2.5 ${
          status === 'done'
            ? direction === 'encrypt' ? 'text-green-500/60' : 'text-amber-500/60'
            : 'text-white/10'
        }`} />
      </div>
    </div>
  );
}
