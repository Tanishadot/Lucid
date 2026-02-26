import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { fadeIn, slideUp } from '../animations/animationVariants';

interface DemoModeProps {
  onExit: () => void;
}

const DemoMode: React.FC<DemoModeProps> = ({ onExit }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedDilemma, setSelectedDilemma] = useState<string | null>(null);

  const dilemmas = [
    "I'm feeling stuck between two career paths and don't know which to choose.",
    "I keep procrastinating on important tasks and feel guilty about it.",
    "My relationships feel shallow, but I'm afraid of deeper connections.",
  ];

  const responses = [
    "What values are you honoring in each of these paths?",
    "What might this procrastination be protecting you from?",
    "What does 'deeper' mean to you in the context of relationships?",
  ];

  const handleDilemmaSelect = (dilemma: string, index: number) => {
    setSelectedDilemma(dilemma);
    setTimeout(() => {
      setCurrentStep(2);
    }, 1000);
  };

  const renderContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <motion.div variants={slideUp} className="text-center">
            <h2 className="text-3xl font-light text-white mb-8">
              How Lucid Thinks
            </h2>
            <p className="text-lg text-gray-300 mb-12 max-w-2xl mx-auto">
              Lucid never gives advice. Instead, it helps you find clarity through 
              thoughtful questions that reveal your own wisdom.
            </p>
            <motion.button
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              onClick={() => setCurrentStep(1)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Try a Sample Reflection
            </motion.button>
          </motion.div>
        );

      case 1:
        return (
          <motion.div variants={slideUp} className="text-center">
            <h3 className="text-2xl font-light text-white mb-8">
              Choose a sample dilemma:
            </h3>
            <div className="space-y-4 max-w-2xl mx-auto">
              {dilemmas.map((dilemma, index) => (
                <motion.button
                  key={index}
                  className="w-full p-4 bg-gray-700 rounded-lg text-left hover:bg-gray-600 transition-colors"
                  onClick={() => handleDilemmaSelect(dilemma, index)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <p className="text-gray-300">{dilemma}</p>
                </motion.button>
              ))}
            </div>
          </motion.div>
        );

      case 2:
        return (
          <motion.div variants={slideUp} className="text-center">
            <div className="mb-8">
              <p className="text-lg text-gray-400 mb-4">You said:</p>
              <p className="text-xl text-blue-300 italic">
                {selectedDilemma}
              </p>
            </div>
            <div className="mb-12">
              <p className="text-lg text-gray-400 mb-4">Lucid responds:</p>
              <p className="text-xl text-white italic">
                {responses[dilemmas.indexOf(selectedDilemma || '')]}
              </p>
            </div>
            <div className="space-x-4">
              <motion.button
                className="px-6 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
                onClick={() => setCurrentStep(1)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Try Another
              </motion.button>
              <motion.button
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                onClick={onExit}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Start Your Conversation
              </motion.button>
            </div>
          </motion.div>
        );

      default:
        return null;
    }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={fadeIn}
      className="min-h-screen bg-gray-900 flex items-center justify-center px-4"
    >
      <div className="max-w-4xl w-full">
        <AnimatePresence mode="wait">
          {renderContent()}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default DemoMode;
