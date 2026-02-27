import React from 'react';
import { motion } from 'framer-motion';

interface PatternMirrorProps {
  patternName: string;
  onExplore?: () => void;
}

const PatternMirror: React.FC<PatternMirrorProps> = ({ patternName, onExplore }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="lucid-card p-6 rounded-lg max-w-md mx-auto mt-6 backdrop-blur-sm bg-white/80 dark:bg-gray-800/80 border border-gray-200/50 dark:border-gray-600/50"
    >
      <div className="text-center">
        <div className="mb-4">
          <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 opacity-20 flex items-center justify-center">
            <span className="text-2xl">🔍</span>
          </div>
        </div>
        
        <h3 className="lucid-primary-text text-lg font-medium mb-3">
          I'm noticing a recurring theme around:
        </h3>
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="lucid-secondary-text text-xl font-semibold mb-4"
        >
          {patternName}
        </motion.div>
        
        <p className="lucid-muted-text text-sm mb-6 leading-relaxed">
          This pattern appears across multiple reflection sessions.
        </p>
        
        {onExplore && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            onClick={onExplore}
            className="lucid-button-secondary w-full"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            Explore this pattern deeper
          </motion.button>
        )}
      </div>
    </motion.div>
  );
};

export default PatternMirror;
