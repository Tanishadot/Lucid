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
      {/* Globe container with existing styling */}
      <div className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-500 rounded-full shadow-lg relative overflow-hidden">
        {/* Circular image mask */}
        <div className="absolute inset-0 rounded-full overflow-hidden">
          <img 
            src="/queen.png" 
            alt="LUCID Mascot"
            className="w-full h-full object-cover"
            style={{
              objectPosition: 'center',
              objectFit: 'cover',
            }}
          />
        </div>
        
        {/* Inner glow effect */}
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
      </div>
    </motion.div>
  );
};

export default Mascot;
