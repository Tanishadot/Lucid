import React from 'react';
import { motion, useInView } from 'framer-motion';
import { AlertCircle, Phone } from 'lucide-react';

const Disclaimer: React.FC = () => {
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });

  return (
    <section ref={ref} className="relative py-16 px-4">
      <div className="container-lucid mx-auto max-w-4xl">
        <motion.div
          className="glass-card p-8 relative overflow-hidden"
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          {/* Glow accent */}
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500/50 via-violet-500/50 to-cyan-500/50" />

          <div className="flex items-start gap-4 mb-6">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center flex-shrink-0">
              <AlertCircle className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-[var(--text-primary)] mb-2">
                Important Disclaimer
              </h3>
              <p className="text-sm text-[var(--text-muted)] leading-relaxed">
                LUCID is a reflection-based AI companion designed to support thoughtful reflection and clarity. 
                It does not provide medical, psychological, legal, or crisis intervention services.
              </p>
            </div>
          </div>

          <div className="space-y-4 text-sm text-[var(--text-muted)] leading-relaxed mb-6">
            <p>
              If you are experiencing severe emotional distress, thoughts of self-harm, or a mental health emergency, 
              please seek professional help immediately.
            </p>
          </div>

          {/* Emergency Helplines */}
          <div className="glass rounded-xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <Phone className="w-4 h-4 text-violet-400" />
              <h4 className="text-sm font-medium text-[var(--text-primary)]">
                India – Emergency & Mental Health Helplines
              </h4>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { name: 'KIRAN Mental Health', number: '1800-599-0019', note: '24/7 Govt.' },
                { name: 'AASRA Suicide Prevention', number: '+91-9820466726', note: '24/7' },
                { name: 'Emergency Services', number: '112', note: 'National' },
              ].map((helpline) => (
                <div
                  key={helpline.name}
                  className="p-3 rounded-lg bg-white/5 border border-white/10 hover:border-violet-500/30 transition-colors"
                >
                  <p className="text-xs text-[var(--text-muted)] mb-1">{helpline.name}</p>
                  <p className="text-sm font-medium text-violet-400">{helpline.number}</p>
                  <p className="text-xs text-[var(--text-muted)] opacity-60">{helpline.note}</p>
                </div>
              ))}
            </div>
          </div>

          <p className="text-xs text-[var(--text-muted)] mt-6 text-center">
            If you are outside India, please contact your local emergency number or a licensed mental health professional in your region.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default Disclaimer;
