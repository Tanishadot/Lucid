import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { fadeIn, float } from '../animations/animationVariants';
import { useParallaxScroll } from '../hooks/useParallaxScroll';

const AtmosphericEntry: React.FC = () => {
  const { style: parallaxStyle } = useParallaxScroll({ speed: 0.2 });
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
      className="min-h-screen lucid-gradient flex flex-col items-center justify-center relative overflow-hidden"
    >
      {/* Parallax sky background elements */}
      <div 
        className="absolute inset-0"
        style={parallaxStyle}
      >
        {/* Floating particles background */}
        {[...Array(20)].map((_, i) => {
          const left = Math.random() * 100;
          const top = Math.random() * 100;
          return (
            <motion.div
              key={i}
              className="absolute w-1 h-1 bg-blue-400 rounded-full opacity-30"
              style={{
                left: `${left}%`,
                top: `${top}%`,
              }}
              animate={float}
              transition={{
                duration: 10 + Math.random() * 10,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
          );
        })}

        {/* Additional atmospheric layers for depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-purple-900/20 via-transparent to-blue-900/20" />
        <div className="absolute inset-0 bg-gradient-to-b from-blue-800/10 via-transparent to-slate-900/10" />
      </div>

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
