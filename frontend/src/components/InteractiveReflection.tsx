import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { fadeIn, slideUp } from '../animations/animationVariants';
import { useParallaxScroll } from '../hooks/useParallaxScroll';

interface InteractiveReflectionProps {
  onPromptClick: (prompt: string) => void;
}

const InteractiveReflection: React.FC<InteractiveReflectionProps> = ({ onPromptClick }) => {
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);
  const [response, setResponse] = useState<string>('');
  const { style: parallaxStyle } = useParallaxScroll({ speed: 0.15 });

  const prompts = [
    "What feels unclear right now?",
    "What patterns do you notice in your thinking?",
    "What assumptions are you making?",
    "What would you explore if you weren't afraid?",
  ];

  const handlePromptClick = (prompt: string) => {
    setSelectedPrompt(prompt);
    setResponse("What perspective might you be missing in this moment?");
    onPromptClick(prompt);
  };

  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={fadeIn}
      className="py-20 px-4 lucid-card relative"
    >
      {/* Subtle parallax background layer */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={parallaxStyle}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-blue-800/5 via-transparent to-purple-800/5 rounded-lg" />
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
        <motion.h2
          className="text-3xl md:text-4xl font-light lucid-primary-text text-center mb-12"
          variants={slideUp}
        >
          A moment of reflection
        </motion.h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {prompts.map((prompt, index) => (
            <motion.button
              key={index}
              className="p-6 lucid-card rounded-lg text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-300"
              variants={slideUp}
              onClick={() => handlePromptClick(prompt)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <p className="text-lg lucid-secondary-text">{prompt}</p>
            </motion.button>
          ))}
        </div>

        {response && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="p-8 lucid-card rounded-lg"
          >
            <p className="text-xl lucid-primary-text text-center italic">{response}</p>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default InteractiveReflection;
