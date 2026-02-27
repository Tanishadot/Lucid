import React from 'react';
import { motion } from 'framer-motion';
import { fadeIn } from '../animations/animationVariants';
import ParallaxBackground from '../components/ParallaxBackground';

const TestParallax: React.FC = () => {
  return (
    <div className="min-h-screen relative">
      {/* Global parallax background */}
      <ParallaxBackground speed={0.2}>
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/30 via-transparent to-blue-900/20" />
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/10 via-transparent to-blue-800/10" />
      </ParallaxBackground>

      {/* Test content sections */}
      <motion.section
        initial="hidden"
        animate="visible"
        variants={fadeIn}
        className="min-h-screen flex items-center justify-center relative z-10"
      >
        <div className="text-center text-white">
          <h1 className="text-6xl font-light mb-4">Scroll Test</h1>
          <p className="text-xl text-blue-300">Scroll down to see parallax effect</p>
        </div>
      </motion.section>

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeIn}
        className="min-h-screen flex items-center justify-center relative z-10"
      >
        <div className="text-center text-white">
          <h2 className="text-5xl font-light mb-4">Section 2</h2>
          <p className="text-lg text-blue-300">Background should be moving slower</p>
        </div>
      </motion.section>

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeIn}
        className="min-h-screen flex items-center justify-center relative z-10"
      >
        <div className="text-center text-white">
          <h2 className="text-5xl font-light mb-4">Section 3</h2>
          <p className="text-lg text-blue-300">Cinematic atmospheric drift</p>
        </div>
      </motion.section>
    </div>
  );
};

export default TestParallax;
