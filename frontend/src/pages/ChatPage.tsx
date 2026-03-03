import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Mascot from '../components/Mascot';
import MicButton from '../components/MicButton';
import SpeakerButton from '../components/SpeakerButton';
import ThemeToggle from '../components/ThemeToggle';
import DepthIndicator from '../components/DepthIndicator';
import PatternMirror from '../components/PatternMirror';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import { useTextToSpeech } from '../hooks/useTextToSpeech';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  depth?: 'surface' | 'pattern' | 'identity' | 'root';
  patternName?: string;
}

interface ChatPageProps {
  onBack: () => void;
}

const ChatPage: React.FC<ChatPageProps> = ({ onBack }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showPatternMirror, setShowPatternMirror] = useState(false);
  const [silenceMode, setSilenceMode] = useState(false);
  const [messageCount, setMessageCount] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Audio recording
  const { 
    isRecording, 
    transcript, 
    isSupported, 
    toggleRecording, 
    error, 
    hasError, 
    clearError,
    isTranscribing,
    clearTranscript
  } = useAudioRecorder();
  
  // Text to speech
  const { isSpeaking, currentMessageId, toggleSpeaking } = useTextToSpeech();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Update input text with transcript when recording stops and transcription is complete
  useEffect(() => {
    if (!isRecording && !isTranscribing && transcript) {
      setInputText(prev => prev + (prev ? ' ' : '') + transcript);
      clearTranscript();
    }
  }, [isRecording, isTranscribing, transcript, clearTranscript]);

  // Detect patterns for mirror mode
  useEffect(() => {
    if (messageCount >= 4 && !showPatternMirror) {
      setShowPatternMirror(true);
    }
  }, [messageCount, showPatternMirror]);

  // Silence mode after strong questions
  useEffect(() => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage && !lastMessage.isUser && lastMessage.text.includes('?')) {
      setSilenceMode(true);
      setTimeout(() => setSilenceMode(false), 8000);
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setMessageCount(prev => prev + 1);
    const messageToSend = inputText;
    setInputText('');
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/reflect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_input: messageToSend,
          session_id: "frontend-session"
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Determine depth based on response content
      let depth: Message['depth'] = 'surface';
      if (data.response.includes('identity') || data.response.includes('behavior')) {
        depth = 'identity';
      } else if (data.response.includes('comparison') || data.response.includes('standard')) {
        depth = 'pattern';
      } else if (data.response.includes('root') || data.response.includes('fundamental')) {
        depth = 'root';
      }

      const reflectionResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        isUser: false,
        timestamp: new Date(),
        depth,
        patternName: depth !== 'surface' ? extractPatternName(data.response) : undefined
      };
      
      setMessages(prev => [...prev, reflectionResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const fallbackResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm having trouble connecting right now. What feels present for you as you wait?",
        isUser: false,
        timestamp: new Date(),
        depth: 'surface'
      };
      
      setMessages(prev => [...prev, fallbackResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  const extractPatternName = (response: string) => {
    const patterns = ['perfectionism', 'visibility', 'approval', 'identity', 'comparison'];
    return patterns.find(pattern => response.toLowerCase().includes(pattern)) || 'Recurring Pattern';
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen lucid-gradient flex flex-col">
      {/* Header */}
      <div className="lucid-surface border-b border-gray-200 dark:border-gray-600 p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <button
            onClick={onBack}
            className="lucid-muted-text hover:lucid-primary-text transition-colors"
          >
            ← Back
          </button>
          <h1 className="text-3xl font-bold lucid-primary-text" style={{ fontFamily: 'Playfair Display, serif' }}>Lucid</h1>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <Mascot />
          </div>
        </div>
      </div>

      {/* Pattern Mirror */}
      <AnimatePresence>
        {showPatternMirror && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            transition={{ duration: 0.5 }}
            className="relative z-20"
          >
            <PatternMirror 
              patternName="Perfectionism and visibility"
              onExplore={() => {
                console.log('Exploring pattern deeper');
              }}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto space-y-6">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-lg p-4 rounded-lg relative ${
                    message.isUser
                      ? 'bg-light-primary-btn dark:bg-dark-primary-btn text-white'
                      : 'lucid-card'
                  } ${currentMessageId === message.id ? 'ring-2 ring-blue-400/50' : ''}`}
                >
                  {/* Depth indicator for AI messages */}
                  {!message.isUser && message.depth && (
                    <div className="absolute -top-3 -right-3">
                      <DepthIndicator depth={message.depth} />
                    </div>
                  )}
                  
                  <motion.p 
                    className="text-sm"
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 }}
                  >
                    {message.text}
                  </motion.p>
                  
                  {/* Speaker button for AI messages */}
                  {!message.isUser && (
                    <div className="absolute bottom-2 right-2">
                      <SpeakerButton
                        isSpeaking={isSpeaking}
                        isCurrentMessage={currentMessageId === message.id}
                        onClick={() => toggleSpeaking(message.text, message.id)}
                      />
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="lucid-card p-4 rounded-lg">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                  <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="lucid-surface border-t border-gray-200 dark:border-gray-600 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="What feels unclear right now?"
                className="w-full px-4 py-3 pr-12 lucid-card rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
                disabled={silenceMode}
              />
              
              {/* Microphone button */}
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                <MicButton
                  isListening={isRecording}
                  isSupported={isSupported}
                  hasError={hasError}
                  onClick={toggleRecording}
                />
              </div>
            </div>
            
            <motion.button
              onClick={handleSendMessage}
              className="lucid-button-primary text-white rounded-lg disabled:opacity-50"
              disabled={!inputText.trim() || isTyping || isRecording || silenceMode}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Send
            </motion.button>
          </div>
          
          {/* Silence mode indicator */}
          <AnimatePresence>
            {silenceMode && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="text-center mt-2"
              >
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 4 }}
                  className="lucid-secondary-text text-sm italic"
                >
                  Sit with this.
                </motion.p>
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Show recording/transcribing status */}
          {(isRecording || isTranscribing) && (
            <div className="mt-2 text-sm lucid-secondary-text italic">
              {isRecording ? 'Recording...' : 'Transcribing...'}
            </div>
          )}
          
          {/* Show transcript while transcribing */}
          {transcript && (
            <div className="mt-2 text-sm lucid-secondary-text italic">
              Transcript: {transcript}
            </div>
          )}
          
          {/* Show error message */}
          {error && (
            <div className="mt-2 p-2 lucid-error rounded-lg">
              <div className="flex items-center justify-between">
                <p className="text-sm">{error}</p>
                <button
                  onClick={clearError}
                  className="ml-4 hover:opacity-80"
                  aria-label="Clear error"
                >
                  ×
                </button>
              </div>
            </div>
          )}
          
          {/* Subtle hint */}
          <div className="text-center mt-2">
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 2 }}
              className="lucid-muted-text text-xs"
            >
              Lucid asks one question at a time.
            </motion.p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
