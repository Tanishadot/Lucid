import React from 'react';
import { motion } from 'framer-motion';
import { fadeIn, glow } from '../animations/animationVariants';

// Crescent orbital icon for "Start a Quiet Conversation"
const CrescentOrbitalIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg
    className={className}
    viewBox="0 0 64 64"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <defs>
      <linearGradient id="crescentGradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="rgba(180,200,255,0.8)" />
        <stop offset="100%" stopColor="rgba(147,197,253,0.6)" />
      </linearGradient>
      <filter id="crescentGlow">
        <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
        <feMerge>
          <feMergeNode in="coloredBlur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    
    {/* Orbital path */}
    <motion.circle
      cx="32"
      cy="32"
      r="24"
      stroke="url(#crescentGradient)"
      strokeWidth="1"
      fill="none"
      opacity="0.3"
      animate={{ rotate: 360 }}
      transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
      style={{ transformOrigin: 'center' }}
    />
    
    {/* Crescent moon */}
    <path
      d="M 32 12 C 24 12 18 18 18 26 C 18 34 24 40 32 40 C 28 38 26 34 26 30 C 26 22 30 14 38 14 C 36 13 34 12 32 12 Z"
      stroke="url(#crescentGradient)"
      strokeWidth="1.5"
      fill="none"
      filter="url(#crescentGlow)"
    />
    
    {/* Central glow point */}
    <circle
      cx="32"
      cy="32"
      r="2"
      fill="url(#crescentGradient)"
      opacity="0.8"
    />
  </svg>
);

// Neural node icon for "See How Lucid Thinks"
const NeuralNodeIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg
    className={className}
    viewBox="0 0 64 64"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <defs>
      <linearGradient id="neuralGradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="rgba(180,200,255,0.8)" />
        <stop offset="100%" stopColor="rgba(147,197,253,0.6)" />
      </linearGradient>
      <filter id="neuralGlow">
        <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
        <feMerge>
          <feMergeNode in="coloredBlur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    
    {/* Neural connections */}
    <motion.line
      x1="20"
      y1="20"
      x2="32"
      y2="32"
      stroke="url(#neuralGradient)"
      strokeWidth="1"
      opacity="0.6"
      animate={{ opacity: [0.6, 1, 0.6] }}
      transition={{ duration: 3, repeat: Infinity }}
    />
    <motion.line
      x1="32"
      y1="32"
      x2="44"
      y2="20"
      stroke="url(#neuralGradient)"
      strokeWidth="1"
      opacity="0.6"
      animate={{ opacity: [0.6, 1, 0.6] }}
      transition={{ duration: 3, repeat: Infinity, delay: 0.5 }}
    />
    <motion.line
      x1="32"
      y1="32"
      x2="44"
      y2="44"
      stroke="url(#neuralGradient)"
      strokeWidth="1"
      opacity="0.6"
      animate={{ opacity: [0.6, 1, 0.6] }}
      transition={{ duration: 3, repeat: Infinity, delay: 1 }}
    />
    <motion.line
      x1="32"
      y1="32"
      x2="20"
      y2="44"
      stroke="url(#neuralGradient)"
      strokeWidth="1"
      opacity="0.6"
      animate={{ opacity: [0.6, 1, 0.6] }}
      transition={{ duration: 3, repeat: Infinity, delay: 1.5 }}
    />
    
    {/* Neural nodes */}
    <circle cx="20" cy="20" r="3" stroke="url(#neuralGradient)" strokeWidth="1" fill="none" filter="url(#neuralGlow)" />
    <circle cx="44" cy="20" r="3" stroke="url(#neuralGradient)" strokeWidth="1" fill="none" filter="url(#neuralGlow)" />
    <circle cx="44" cy="44" r="3" stroke="url(#neuralGradient)" strokeWidth="1" fill="none" filter="url(#neuralGlow)" />
    <circle cx="20" cy="44" r="3" stroke="url(#neuralGradient)" strokeWidth="1" fill="none" filter="url(#neuralGlow)" />
    <circle cx="32" cy="32" r="4" stroke="url(#neuralGradient)" strokeWidth="1.5" fill="none" filter="url(#neuralGlow)" />
  </svg>
);

interface DualEntryButtonsProps {
  onStartChat: () => void;
  onStartDemo: () => void;
}

const DualEntryButtons: React.FC<DualEntryButtonsProps> = ({ onStartChat, onStartDemo }) => {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={fadeIn}
      className="py-20 px-4 relative"
    >
      {/* Subtle depth overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-transparent dark:from-slate-900/3 dark:via-blue-950/3 dark:to-purple-950/3 light:from-white/3 light:via-blue-50/3 light:to-purple-50/3" />
      <div className="max-w-4xl mx-auto relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <motion.button
            className="group relative p-8 lucid-card rounded-lg border border-gray-200/30 dark:border-gray-600/30 hover:border-blue-500/50 transition-all duration-300 backdrop-blur-sm bg-white/5 dark:bg-black/10 shadow-lg hover:shadow-xl"
            variants={glow}
            onClick={onStartChat}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
          >
            {/* Gradient border effect */}
            <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            {/* Inner glow on hover */}
            <div className="absolute inset-0 rounded-lg bg-gradient-to-t from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            <div className="relative text-center">
              <div className="mb-4 flex justify-center">
                <CrescentOrbitalIcon className="w-16 h-16" />
              </div>
              <h3 className="text-xl font-semibold lucid-primary-text mb-2">
                Start a Quiet Conversation
              </h3>
              <p className="lucid-muted-text text-sm">
                Begin your reflective journey with Lucid
              </p>
            </div>
            <motion.div
              className="absolute inset-0 rounded-lg bg-blue-500 opacity-0 group-hover:opacity-5"
              initial={false}
              animate={{ opacity: [0, 0.05, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.button>

          <motion.button
            className="group relative p-8 lucid-card rounded-lg border border-gray-200/30 dark:border-gray-600/30 hover:border-blue-500/50 transition-all duration-300 backdrop-blur-sm bg-white/5 dark:bg-black/10 shadow-lg hover:shadow-xl"
            variants={glow}
            onClick={onStartDemo}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
          >
            {/* Gradient border effect */}
            <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-purple-500/10 via-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            {/* Inner glow on hover */}
            <div className="absolute inset-0 rounded-lg bg-gradient-to-t from-purple-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            <div className="relative text-center">
              <div className="mb-4 flex justify-center">
                <NeuralNodeIcon className="w-16 h-16" />
              </div>
              <h3 className="text-xl font-semibold lucid-primary-text mb-2">
                See How Lucid Thinks
              </h3>
              <p className="lucid-muted-text text-sm">
                Experience the reflection-first approach
              </p>
            </div>
            <motion.div
              className="absolute inset-0 rounded-lg bg-purple-500 opacity-0 group-hover:opacity-5"
              initial={false}
              animate={{ opacity: [0, 0.05, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

export default DualEntryButtons;
