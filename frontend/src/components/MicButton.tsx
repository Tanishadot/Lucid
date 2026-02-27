import React from 'react';
import { motion } from 'framer-motion';

interface MicButtonProps {
  isListening: boolean;
  isSupported: boolean;
  hasError: boolean;
  onClick: () => void;
  className?: string;
}

const MicButton: React.FC<MicButtonProps> = ({ 
  isListening, 
  isSupported, 
  hasError,
  onClick, 
  className = "" 
}) => {
  if (!isSupported) {
    return (
      <div className="relative group">
        <button
          className={`p-3 rounded-full lucid-button-secondary cursor-not-allowed ${className}`}
          disabled
          aria-label="Voice input not supported"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        </button>
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 lucid-card text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
          Voice input not supported in this browser
        </div>
      </div>
    );
  }

  return (
    <motion.button
      onClick={onClick}
      className={`p-3 rounded-full transition-all duration-200 ${className} ${
        hasError
          ? 'bg-orange-500 text-white'
          : isListening 
            ? 'bg-red-500 text-white scale-105' 
            : 'lucid-button-secondary'
      }`}
      whileHover={{ scale: isListening ? 1.05 : 1.02 }}
      whileTap={{ scale: 0.95 }}
      aria-label={isListening ? "Stop recording" : "Start voice input"}
    >
      <div className="relative">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
        
        {isListening && (
          <motion.div
            className="absolute inset-0 rounded-full bg-red-400 opacity-30"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.3, 0.1, 0.3],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        )}
        
        {isListening && (
          <div className="absolute top-0 right-0 w-2 h-2 bg-red-600 rounded-full" />
        )}
        
        {hasError && (
          <div className="absolute top-0 right-0 w-2 h-2 bg-orange-300 rounded-full" />
        )}
      </div>
    </motion.button>
  );
};

export default MicButton;
