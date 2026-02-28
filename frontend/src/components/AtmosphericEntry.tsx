import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { fadeIn } from '../animations/animationVariants';

const AtmosphericEntry: React.FC = () => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Check if dark mode is active
    const checkDarkMode = () => {
      setIsDark(document.documentElement.classList.contains('dark'));
    };
    
    checkDarkMode();
    
    // Listen for theme changes
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });
    
    return () => observer.disconnect();
  }, []);

  // Define glow colors based on theme
  const glowColors = isDark 
    ? ['0 0 0px rgba(165, 180, 252, 0)', '0 0 14px rgba(165, 180, 252, 0.6)', '0 0 0px rgba(165, 180, 252, 0)']
    : ['0 0 0px rgba(109, 93, 211, 0)', '0 0 12px rgba(109, 93, 211, 0.4)', '0 0 0px rgba(109, 93, 211, 0)'];

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={fadeIn}
      className="min-h-screen flex flex-col items-center justify-center relative"
    >
      {/* Subtle depth overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-transparent dark:from-slate-900/5 dark:via-blue-950/5 dark:to-purple-950/5 light:from-white/5 light:via-blue-50/5 light:to-purple-50/5" />

      {/* Main content */}
      <motion.div
        className="text-center z-10 px-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5 }}
      >
        <motion.h1
          className="text-4xl md:text-6xl font-light lucid-primary-text mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 2, delay: 0.5 }}
        >
          What if clarity didn't come from answers…
        </motion.h1>
        <motion.h2
          className="text-3xl md:text-5xl font-light lucid-secondary-text"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 2, delay: 2 }}
        >
          but from better questions?
        </motion.h2>
        <motion.h3
          className="text-3xl md:text-5xl font-bold lucid-primary-text mt-4"
          style={{ fontFamily: 'Playfair Display, serif' }}
          initial={{ opacity: 0, y: 10 }}
          animate={{ 
            opacity: 1, 
            y: 0,
            textShadow: glowColors
          }}
          transition={{ 
            opacity: { duration: 2, delay: 4 },
            y: { duration: 2, delay: 4 },
            textShadow: { duration: 1.5, delay: 4.5 }
          }}
        >
          LUCID
        </motion.h3>
      </motion.div>

      {/* Breathing glow effect */}
      <motion.div
        className="absolute bottom-10 left-1/2 transform -translate-x-1/2 w-32 h-32 bg-blue-500 rounded-full opacity-20 blur-xl"
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.2, 0.4, 0.2],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    </motion.div>
  );
};

export default AtmosphericEntry;
