import React from 'react';
import { motion } from 'framer-motion';

const Mascot: React.FC = () => {
  return (
    <motion.div
      className="w-24 h-24 relative"
      animate={{
        scale: [1, 1.1, 1],
        opacity: [0.7, 0.9, 0.7],
      }}
      transition={{
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    >
      {/* Simple circle mascot with breathing effect */}
      <div className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-500 rounded-full shadow-lg" />
      <motion.div
        className="absolute inset-2 bg-white rounded-full opacity-30"
        animate={{
          scale: [1, 0.8, 1],
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

export default Mascot;
