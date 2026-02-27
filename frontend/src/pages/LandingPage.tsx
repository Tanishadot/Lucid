import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import AtmosphericEntry from '../components/AtmosphericEntry';
import InteractiveReflection from '../components/InteractiveReflection';
import DualEntryButtons from '../components/DualEntryButtons';
import Mascot from '../components/Mascot';
import ParallaxBackground from '../components/ParallaxBackground';
import Disclaimer from '../components/Disclaimer';
import ThemeToggle from '../components/ThemeToggle';
import ReflectionTimeline from '../components/ReflectionTimeline';

interface LandingPageProps {
  onStartChat: () => void;
  onStartDemo: () => void;
}

interface ReflectionSession {
  id: string;
  sessionNumber: number;
  patternName: string;
  question: string;
  createdAt: Date;
}

const LandingPage: React.FC<LandingPageProps> = ({ onStartChat, onStartDemo }) => {
  const [showTimeline, setShowTimeline] = useState(false);
  
  // Mock reflection sessions for demo
  const mockSessions: ReflectionSession[] = [
    {
      id: '1',
      sessionNumber: 1,
      patternName: 'Fear of disappointing others',
      question: 'What makes their disappointment your responsibility?',
      createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000) // 2 days ago
    },
    {
      id: '2',
      sessionNumber: 2,
      patternName: 'Perfection and visibility',
      question: 'What standard creates the belief of being "not good enough"?',
      createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000) // 5 days ago
    },
    {
      id: '3',
      sessionNumber: 3,
      patternName: 'Parental approval loop',
      question: 'What makes external approval necessary for self-worth?',
      createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) // 7 days ago
    }
  ];

  const handlePromptClick = (prompt: string) => {
    console.log('Prompt clicked:', prompt);
  };

  const handleSessionClick = (session: ReflectionSession) => {
    console.log('Session clicked:', session);
    // Navigate to chat with session context
    onStartChat();
  };

  return (
    <div className="min-h-screen relative flex">
      {/* Main content */}
      <div className={`flex-1 transition-all duration-500 ${showTimeline ? 'mr-80' : 'mr-0'}`}>
        <div className="min-h-screen relative">
          {/* Global parallax sky background */}
          <ParallaxBackground speed={0.1}>
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/30 via-transparent to-blue-900/20" />
            <div className="absolute inset-0 bg-gradient-to-br from-purple-900/10 via-transparent to-blue-800/10" />
          </ParallaxBackground>

          {/* Theme toggle button */}
          <div className="fixed top-8 right-8 z-50">
            <ThemeToggle />
          </div>

          <AtmosphericEntry />
          <InteractiveReflection onPromptClick={handlePromptClick} />
          <DualEntryButtons onStartChat={onStartChat} onStartDemo={onStartDemo} />
          <Disclaimer />
          <div className="fixed bottom-8 right-8">
            <Mascot />
          </div>
        </div>
      </div>

      {/* Reflection Timeline Panel */}
      <AnimatePresence>
        {showTimeline && (
          <motion.div
            initial={{ opacity: 0, x: 320 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 320 }}
            transition={{ duration: 0.5, ease: 'easeInOut' }}
            className="fixed right-0 top-0 h-full w-80 lucid-surface border-l border-gray-200 dark:border-gray-600 z-30 overflow-hidden"
          >
            <div className="h-full flex flex-col">
              {/* Header */}
              <div className="p-4 border-b border-gray-200 dark:border-gray-600">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold lucid-primary-text">Reflection Journey</h2>
                  <button
                    onClick={() => setShowTimeline(false)}
                    className="lucid-muted-text hover:lucid-primary-text transition-colors p-1 rounded"
                  >
                    ×
                  </button>
                </div>
              </div>

              {/* Timeline */}
              <div className="flex-1 overflow-y-auto p-4">
                <ReflectionTimeline 
                  sessions={mockSessions}
                  onSessionClick={handleSessionClick}
                />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Timeline Toggle Button */}
      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 1 }}
        onClick={() => setShowTimeline(!showTimeline)}
        className={`fixed left-4 top-1/2 transform -translate-y-1/2 z-20 p-3 rounded-full lucid-button-secondary shadow-lg ${
          showTimeline ? 'bg-blue-500 text-white' : ''
        }`}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m0 0l-3-3v4M5 12H3" />
        </svg>
      </motion.button>
    </div>
  );
};

export default LandingPage;
