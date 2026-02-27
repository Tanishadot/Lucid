import React from 'react';
import { motion } from 'framer-motion';

interface DepthIndicatorProps {
  depth: 'surface' | 'pattern' | 'identity' | 'root';
  className?: string;
}

const DepthIndicator: React.FC<DepthIndicatorProps> = ({ depth, className = "" }) => {
  const depthConfig = {
    surface: {
      icon: '🌊',
      label: 'Surface',
      color: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
    },
    pattern: {
      icon: '🌊',
      label: 'Pattern',
      color: 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300'
    },
    identity: {
      icon: '🌊',
      label: 'Identity',
      color: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300'
    },
    root: {
      icon: '🌊',
      label: 'Root',
      color: 'bg-pink-100 text-pink-700 dark:bg-pink-900 dark:text-pink-300'
    }
  };

  const config = depthConfig[depth];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${config.color} ${className}`}
    >
      <span className="text-base">{config.icon}</span>
      <span>{config.label}</span>
    </motion.div>
  );
};

export default DepthIndicator;
