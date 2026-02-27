import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface ReflectionSession {
  id: string;
  sessionNumber: number;
  patternName: string;
  question: string;
  createdAt: Date;
}

interface ReflectionTimelineProps {
  sessions: ReflectionSession[];
  onSessionClick?: (session: ReflectionSession) => void;
}

const ReflectionTimeline: React.FC<ReflectionTimelineProps> = ({ sessions, onSessionClick }) => {
  const [expandedSession, setExpandedSession] = useState<string | null>(null);

  const getTimeAgo = (date: Date) => {
    const now = new Date();
    const diffInMs = now.getTime() - date.getTime();
    const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
    
    if (diffInDays === 0) return 'Today';
    if (diffInDays === 1) return '1 day ago';
    if (diffInDays < 7) return `${diffInDays} days ago`;
    if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`;
    return `${Math.floor(diffInDays / 30)} months ago`;
  };

  return (
    <div className="flex flex-col space-y-4 p-6">
      {sessions.length === 0 ? (
        <div className="text-center py-12">
          <p className="lucid-muted-text text-lg">Your reflection journey begins here.</p>
        </div>
      ) : (
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-200 to-blue-300 dark:from-blue-800 dark:to-blue-900" />
          
          {/* Session nodes */}
          <div className="relative z-10">
            {sessions.map((session, index) => (
              <motion.div
                key={session.id}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="relative"
              >
                {/* Node */}
                <motion.div
                  className={`w-12 h-12 rounded-full border-2 cursor-pointer transition-all duration-300 ${
                    expandedSession === session.id 
                      ? 'bg-blue-500 border-blue-600 shadow-lg shadow-blue-500/50' 
                      : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 hover:shadow-md hover:shadow-blue-500/30'
                  }`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    setExpandedSession(expandedSession === session.id ? null : session.id);
                    onSessionClick?.(session);
                  }}
                >
                  <div className="flex items-center justify-center w-full h-full">
                    <span className={`text-xs font-medium ${
                      expandedSession === session.id ? 'text-white' : 'lucid-primary-text'
                    }`}>
                      {session.sessionNumber}
                    </span>
                  </div>
                </motion.div>

                {/* Session info */}
                <div className="ml-16 mt-2">
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ 
                      opacity: expandedSession === session.id ? 1 : 0.3,
                      y: expandedSession === session.id ? 0 : -10
                    }}
                    transition={{ duration: 0.3 }}
                    className="lucid-card p-4 rounded-lg max-w-xs"
                  >
                    <h4 className="font-semibold lucid-primary-text text-sm mb-1">
                      {session.patternName}
                    </h4>
                    <p className="lucid-muted-text text-xs mb-2">
                      {getTimeAgo(session.createdAt)}
                    </p>
                    <p className="lucid-body text-sm leading-relaxed">
                      {session.question}
                    </p>
                  </motion.div>
                </div>

                {/* Connector line */}
                {index < sessions.length - 1 && (
                  <div className="absolute left-6 top-12 w-0.5 h-8 bg-gradient-to-b from-blue-200 to-blue-300 dark:from-blue-800 dark:to-blue-900" />
                )}
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReflectionTimeline;
