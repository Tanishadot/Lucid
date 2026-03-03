import React from 'react';
import { motion } from 'framer-motion';

const NeuralFooter: React.FC = () => {
  return (
    <footer className="relative py-16 px-6 overflow-hidden">
      {/* Neural network lines fading into darkness */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Left side neural lines */}
        <svg
          className="absolute bottom-0 left-0 w-full h-64"
          viewBox="0 0 1200 256"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="neuralGradient" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="rgba(176, 75, 163, 0.3)" />
              <stop offset="50%" stopColor="rgba(124, 92, 255, 0.15)" />
              <stop offset="100%" stopColor="transparent" />
            </linearGradient>
          </defs>
          
          {/* Main neural lines */}
          <motion.path
            d="M0,256 Q150,200 300,220 T600,180 T900,200 T1200,128"
            fill="none"
            stroke="url(#neuralGradient)"
            strokeWidth="1"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: 'easeInOut' }}
          />
          <motion.path
            d="M0,256 Q100,180 250,200 T500,160 T800,180 T1200,100"
            fill="none"
            stroke="url(#neuralGradient)"
            strokeWidth="0.5"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 0.6 }}
            transition={{ duration: 3, delay: 0.5, ease: 'easeInOut' }}
          />
          <motion.path
            d="M0,256 Q200,220 400,200 T700,160 T1000,140 T1200,80"
            fill="none"
            stroke="url(#neuralGradient)"
            strokeWidth="0.5"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 0.5 }}
            transition={{ duration: 3, delay: 1, ease: 'easeInOut' }}
          />
        </svg>

        {/* Pulsating heartbeat dot */}
        <motion.div
          className="absolute bottom-8 right-8"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.5, 1, 0.5],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <div className="w-2 h-2 rounded-full bg-magenta-500 shadow-[0_0_10px_rgba(176,75,163,0.8)]" />
        </motion.div>
      </div>

      {/* Footer content */}
      <div className="container-lucid relative z-10">
        <motion.div
          className="flex flex-col items-center justify-center text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          {/* Logo */}
          <motion.div
            className="mb-6"
            whileHover={{ scale: 1.05 }}
          >
            <span className="text-2xl font-light tracking-widest text-magenta-500">
              LUCID
            </span>
          </motion.div>

          {/* Tagline */}
          <p className="text-sm text-[var(--text-muted)] mb-8 max-w-md">
            An AI companion for cognitive reflection and personal growth.
          </p>

          {/* Links */}
          <div className="flex items-center gap-8 mb-8">
            {['About', 'Privacy', 'Terms', 'Contact'].map((link, index) => (
              <motion.a
                key={link}
                href="#"
                className="text-sm text-[var(--text-muted)] hover:text-magenta-500 transition-colors"
                whileHover={{ y: -2 }}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                {link}
              </motion.a>
            ))}
          </div>

          {/* Copyright */}
          <p className="text-xs text-[var(--text-muted)] opacity-60">
            &copy; 2024 LUCID. All rights reserved.
          </p>
        </motion.div>
      </div>

      {/* Bottom fade to black */}
      <div 
        className="absolute bottom-0 left-0 right-0 h-32 pointer-events-none"
        style={{
          background: 'linear-gradient(to top, var(--bg-primary), transparent)',
        }}
      />
    </footer>
  );
};

export default NeuralFooter;
