import React from 'react';
import { motion } from 'framer-motion';
import { fadeIn, float } from '../animations/animationVariants';

const AtmosphericEntry: React.FC = () => {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={fadeIn}
      className="min-h-screen bg-gray-900 flex flex-col items-center justify-center relative overflow-hidden"
    >
      {/* Floating particles background */}
      <div className="absolute inset-0">
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
      </div>

      {/* Main content */}
      <motion.div
        className="text-center z-10 px-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5 }}
      >
        <motion.h1
          className="text-4xl md:text-6xl font-light text-white mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 2, delay: 0.5 }}
        >
          What if clarity didn't come from answers…
        </motion.h1>
        <motion.h2
          className="text-3xl md:text-5xl font-light text-blue-300"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 2, delay: 2 }}
        >
          but from better questions?
        </motion.h2>
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
