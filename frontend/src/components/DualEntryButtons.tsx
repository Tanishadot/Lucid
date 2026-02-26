import React from 'react';
import { motion } from 'framer-motion';
import { fadeIn, glow } from '../animations/animationVariants';

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
      className="py-20 px-4 bg-slate-800/50"
    >
      <div className="max-w-4xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <motion.button
            className="group relative p-8 lucid-card rounded-lg border border-slate-700/50 hover:border-blue-500 transition-all duration-300"
            variants={glow}
            onClick={onStartChat}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="text-center">
              <span className="text-4xl mb-4 block">🌙</span>
              <h3 className="text-xl font-semibold text-white mb-2">
                Start a Quiet Conversation
              </h3>
              <p className="text-gray-400 text-sm">
                Begin your reflective journey with Lucid
              </p>
            </div>
            <motion.div
              className="absolute inset-0 rounded-lg bg-blue-500 opacity-0 group-hover:opacity-10"
              initial={false}
              animate={{ opacity: [0, 0.1, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.button>

          <motion.button
            className="group relative p-8 lucid-card rounded-lg border border-slate-700/50 hover:border-purple-500 transition-all duration-300"
            variants={glow}
            onClick={onStartDemo}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="text-center">
              <span className="text-4xl mb-4 block">📖</span>
              <h3 className="text-xl font-semibold text-white mb-2">
                See How Lucid Thinks
              </h3>
              <p className="text-gray-400 text-sm">
                Experience the reflection-first approach
              </p>
            </div>
            <motion.div
              className="absolute inset-0 rounded-lg bg-purple-500 opacity-0 group-hover:opacity-10"
              initial={false}
              animate={{ opacity: [0, 0.1, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

export default DualEntryButtons;
