import React from 'react';
import { motion } from 'framer-motion';

const AmbientLight: React.FC = () => {
  const beams = [
    { left: '10%', delay: 0, duration: 20 },
    { left: '25%', delay: 5, duration: 25 },
    { left: '40%', delay: 10, duration: 18 },
    { left: '60%', delay: 3, duration: 22 },
    { left: '75%', delay: 8, duration: 20 },
    { left: '90%', delay: 15, duration: 24 },
  ];

  const lights = [
    { x: 0.2, y: 0.3, radius: 0.4, color: 'rgba(156, 134, 216, 0.02)' },
    { x: 0.8, y: 0.7, radius: 0.3, color: 'rgba(236, 72, 153, 0.015)' },
    { x: 0.5, y: 0.1, radius: 0.5, color: 'rgba(234, 179, 248, 0.02)' },
  ];

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {beams.map((beam, index) => (
        <motion.div
          key={index}
          className="absolute top-0 w-[2px] h-[200%]"
          style={{
            left: beam.left,
            background: `linear-gradient(180deg, 
              transparent 0%, 
              ${lights[0].color} 20%, 
              ${lights[1].color} 50%, 
              ${lights[2].color} 80%, 
              transparent 100%
            )`,
          }}
          initial={{ 
            y: '-50%', 
            opacity: 0,
            rotate: 15 
          }}
          animate={{ 
            y: ['-50%', '0%'],
            opacity: [0, 1, 1, 0],
          }}
          transition={{
            y: {
              duration: beam.duration,
              repeat: Infinity,
              ease: 'linear',
              delay: beam.delay,
            },
            opacity: {
              duration: beam.duration,
              repeat: Infinity,
              ease: 'linear',
              delay: beam.delay,
              times: [0, 0.1, 0.9, 1],
            }
          }}
        />
      ))}

      {/* Additional ambient glow spots */}
      <motion.div
        className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(139, 92, 246, 0.08) 0%, transparent 60%)',
          filter: 'blur(60px)',
        }}
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3],
          x: [0, 30, 0],
          y: [0, -20, 0],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />

      <motion.div
        className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 60%)',
          filter: 'blur(50px)',
        }}
        animate={{
          scale: [1, 1.15, 1],
          opacity: [0.3, 0.45, 0.3],
          x: [0, -20, 0],
          y: [0, 30, 0],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 3,
        }}
      />

      <motion.div
        className="absolute top-1/2 right-1/3 w-64 h-64 rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(6, 182, 212, 0.06) 0%, transparent 60%)',
          filter: 'blur(40px)',
        }}
        animate={{
          scale: [1, 1.25, 1],
          opacity: [0.2, 0.4, 0.2],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 6,
        }}
      />
    </div>
  );
};

export default AmbientLight;
