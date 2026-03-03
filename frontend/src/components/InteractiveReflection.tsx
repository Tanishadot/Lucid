import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { MessageCircle, Lightbulb, Brain, Eye } from 'lucide-react';

interface InteractiveReflectionProps {
  onPromptClick: (prompt: string) => void;
}

const InteractiveReflection: React.FC<InteractiveReflectionProps> = ({ onPromptClick }) => {
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.2 });

  const features = [
    {
      icon: MessageCircle,
      title: 'Conversational',
      description: 'Natural dialogue that feels like talking to a thoughtful friend',
    },
    {
      icon: Lightbulb,
      title: 'Insightful',
      description: 'Questions that illuminate patterns you might have missed',
    },
    {
      icon: Brain,
      title: 'Cognitive',
      description: 'Designed to enhance self-awareness and mental clarity',
    },
    {
      icon: Eye,
      title: 'Reflective',
      description: 'A mirror for your thoughts, not a source of answers',
    },
  ];

  const prompts = [
    "What feels unclear right now?",
    "What patterns do you notice in your thinking?",
    "What assumptions are you making?",
    "What would you explore if you weren't afraid?",
  ];

  const handlePromptClick = (prompt: string) => {
    setSelectedPrompt(prompt);
    onPromptClick(prompt);
  };

  return (
    <section ref={ref} className="relative py-24 px-4">
      <div className="container-lucid mx-auto">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-4xl md:text-5xl font-light text-gradient mb-4">
            A moment of reflection
          </h2>
          <p className="text-[var(--text-muted)] max-w-xl mx-auto">
            Explore questions designed to deepen your self-awareness and understanding
          </p>
        </motion.div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              className="glass-card p-6 group cursor-default"
              initial={{ opacity: 0, y: 30, filter: 'blur(10px)' }}
              animate={isInView ? { opacity: 1, y: 0, filter: 'blur(0px)' } : {}}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -8, scale: 1.02 }}
            >
              <motion.div
                className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-violet-500/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform"
              >
                <feature.icon className="w-6 h-6 text-violet-400 icon-breathe" />
              </motion.div>
              <h3 className="text-lg font-medium text-[var(--text-primary)] mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-[var(--text-muted)]">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Prompt Cards */}
        <motion.div
          className="max-w-3xl mx-auto"
          initial={{ opacity: 0 }}
          animate={isInView ? { opacity: 1 } : {}}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <h3 className="text-center text-xl text-[var(--text-secondary)] mb-8">
            Begin with a question
          </h3>
          
          <div className="grid grid-cols-4 gap-4">
            {prompts.map((prompt, index) => (
              <motion.button
                key={index}
                className={`glass-card p-6 text-left relative overflow-hidden group ${
                  selectedPrompt === prompt ? 'border-violet-500/50' : ''
                }`}
                initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
                animate={isInView ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.5 + index * 0.1 }}
                onClick={() => handlePromptClick(prompt)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {/* Hover glow effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-violet-500/10 to-blue-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                <p className="text-[var(--text-secondary)] group-hover:text-[var(--text-primary)] transition-colors relative z-10">
                  {prompt}
                </p>
                
                {/* Subtle arrow indicator */}
                <motion.div
                  className="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity"
                  initial={{ x: -10 }}
                  whileHover={{ x: 0 }}
                >
                  <span className="text-violet-400">→</span>
                </motion.div>
              </motion.button>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default InteractiveReflection;
