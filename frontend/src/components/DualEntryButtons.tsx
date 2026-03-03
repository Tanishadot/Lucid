import React from 'react';
import { motion, useInView } from 'framer-motion';
import GlowingButton from './GlowingButton';
import { MessageSquare, Play } from 'lucide-react';

interface DualEntryButtonsProps {
  onStartChat: () => void;
  onStartDemo: () => void;
}

const DualEntryButtons: React.FC<DualEntryButtonsProps> = ({ onStartChat, onStartDemo }) => {
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });

  const options = [
    {
      icon: MessageSquare,
      title: 'Start a Quiet Conversation',
      description: 'Begin your reflective journey with Lucid through natural dialogue',
      action: onStartChat,
      variant: 'primary' as const,
      delay: 0,
    },
    {
      icon: Play,
      title: 'See How Lucid Thinks',
      description: 'Experience the reflection-first approach in action',
      action: onStartDemo,
      variant: 'secondary' as const,
      delay: 0.15,
    },
  ];

  return (
    <section ref={ref} className="relative py-24 px-4">
      <div className="container-lucid mx-auto max-w-4xl">
        {/* Section Header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-light text-gradient mb-4">
            How would you like to begin?
          </h2>
          <p className="text-[var(--text-muted)]">
            Choose your path into cognitive reflection
          </p>
        </motion.div>

        {/* Entry Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {options.map((option) => (
            <motion.div
              key={option.title}
              className="glass-card p-8 group cursor-pointer relative overflow-hidden"
              initial={{ opacity: 0, y: 40, filter: 'blur(10px)' }}
              animate={isInView ? { opacity: 1, y: 0, filter: 'blur(0px)' } : {}}
              transition={{ duration: 0.7, delay: option.delay }}
              whileHover={{ y: -8, scale: 1.02 }}
              onClick={option.action}
            >
              {/* Animated gradient border on hover */}
              <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                <div className="absolute inset-0 rounded-2xl p-[1px] bg-gradient-to-r from-blue-500/50 via-violet-500/50 to-blue-500/50" />
              </div>

              {/* Glow effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-violet-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl" />

              <div className="relative z-10">
                {/* Icon */}
                <motion.div
                  className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500/20 to-violet-500/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
                  whileHover={{ rotate: 5 }}
                >
                  <option.icon className="w-7 h-7 text-violet-400" />
                </motion.div>

                {/* Content */}
                <h3 className="text-xl font-medium text-[var(--text-primary)] mb-3">
                  {option.title}
                </h3>
                <p className="text-[var(--text-muted)] text-sm leading-relaxed mb-6">
                  {option.description}
                </p>

                {/* CTA */}
                <GlowingButton
                  size="md"
                  variant={option.variant}
                  onClick={() => option.action()}
                >
                  {option.variant === 'primary' ? 'Start Conversation' : 'Watch Demo'}
                </GlowingButton>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default DualEntryButtons;
