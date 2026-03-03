import React, { useEffect, useState } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import NeuralBrain from './NeuralBrain';
import GlowingButton from './GlowingButton';
import { Sparkles, ArrowDown } from 'lucide-react';

interface AtmosphericEntryProps {
  onStartChat?: () => void;
  onStartDemo?: () => void;
}

const AtmosphericEntry: React.FC<AtmosphericEntryProps> = ({ onStartChat, onStartDemo }) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const { scrollY } = useScroll();
  
  // Parallax transforms
  const brainY = useTransform(scrollY, [0, 500], [0, 100]);
  const textY = useTransform(scrollY, [0, 500], [0, 50]);
  const opacity = useTransform(scrollY, [0, 400], [1, 0]);

  useEffect(() => {
    const timer = setTimeout(() => setIsLoaded(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30, filter: 'blur(10px)' },
    visible: {
      opacity: 1,
      y: 0,
      filter: 'blur(0px)',
      transition: {
        duration: 1,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Neural Brain Background */}
      <motion.div 
        className="absolute inset-0 z-0"
        style={{ y: brainY }}
      >
        <NeuralBrain />
      </motion.div>

      {/* Content Overlay */}
      <motion.div 
        className="relative z-20 text-center px-4 max-w-5xl mx-auto"
        style={{ y: textY, opacity }}
        variants={containerVariants}
        initial="hidden"
        animate={isLoaded ? "visible" : "hidden"}
      >
        {/* Badge */}
        <motion.div
          variants={itemVariants}
          className="inline-flex items-center gap-2 px-4 py-2 mb-8 rounded-full transition-colors duration-300 badge-light-mode"
          style={{
            backdropFilter: 'blur(10px)',
          }}
        >
          <span className="text-sm tracking-wide font-medium">
            AI Cognitive Reflection Companion
          </span>
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          variants={itemVariants}
          className="text-5xl md:text-7xl lg:text-8xl font-light tracking-tight mb-6"
        >
          <span className="text-gradient">Think.</span>
          <span className="text-[var(--text-primary)] mx-4">Reflect.</span>
          <span className="text-gradient">Evolve.</span>
        </motion.h1>

        {/* LUCID Brand */}
        <motion.div
          variants={itemVariants}
          className="mb-8"
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-light tracking-widest text-gradient">
            LUCID
          </h2>
        </motion.div>

        <motion.p
          variants={itemVariants}
          className="text-base text-[var(--text-muted)] mb-12 max-w-xl mx-auto leading-relaxed"
        >
          Discover deeper insights through meaningful conversations that help you understand your thoughts, patterns, and potential.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <GlowingButton 
            onClick={onStartChat}
            size="lg"
            variant="primary"
            className="text-[var(--text-primary)]"
          >
            <Sparkles className="w-5 h-5" />
            Begin Your Journey
          </GlowingButton>
          
          <GlowingButton 
            onClick={onStartDemo}
            size="lg"
            variant="secondary"
          >
            See How It Works
          </GlowingButton>
        </motion.div>

        {/* Scroll Indicator */}
        <motion.div
          variants={itemVariants}
          className="absolute bottom-12 left-1/2 -translate-x-1/2"
        >
          <motion.div
            className="flex flex-col items-center gap-2 text-[var(--text-muted)]"
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          >
            <span className="text-xs tracking-widest uppercase">Explore</span>
            <ArrowDown className="w-4 h-4" />
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Gradient overlay at bottom for smooth transition */}
      <div 
        className="absolute bottom-0 left-0 right-0 h-32 pointer-events-none z-10"
        style={{
          background: 'linear-gradient(to top, var(--bg-primary), transparent)',
        }}
      />
    </section>
  );
};

export default AtmosphericEntry;
