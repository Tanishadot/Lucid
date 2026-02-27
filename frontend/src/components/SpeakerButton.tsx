import React from 'react';
import { motion } from 'framer-motion';

interface SpeakerButtonProps {
  isSpeaking: boolean;
  isCurrentMessage: boolean;
  onClick: () => void;
  className?: string;
}

const SpeakerButton: React.FC<SpeakerButtonProps> = ({ 
  isSpeaking, 
  isCurrentMessage, 
  onClick, 
  className = "" 
}) => {
  return (
    <motion.button
      onClick={onClick}
      className={`p-2 rounded-full transition-all duration-200 opacity-70 hover:opacity-100 ${className} ${
        isCurrentMessage ? 'lucid-secondary-text' : 'lucid-muted-text'
      } hover:bg-gray-100 dark:hover:bg-gray-700`}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      aria-label={isCurrentMessage ? "Stop speaking" : "Read message aloud"}
    >
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        {isCurrentMessage ? (
          // Stop/square icon
          <rect x="6" y="6" width="12" height="12" strokeWidth={2} />
        ) : (
          // Speaker icon
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
        )}
      </svg>
    </motion.button>
  );
};

export default SpeakerButton;
