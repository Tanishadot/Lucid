import React from 'react';
import { motion } from 'framer-motion';
import MicButton from '../components/MicButton';
import { useAudioRecorder } from '../hooks/useAudioRecorder';

const AudioRecorderTest: React.FC = () => {
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

  return (
    <div className="min-h-screen lucid-gradient flex flex-col items-center justify-center p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="lucid-card p-8 max-w-2xl w-full"
      >
        <h1 className="text-2xl font-light text-white mb-8 text-center">Audio Recorder Test</h1>
        
        {/* Status Information */}
        <div className="mb-6 p-4 bg-slate-700/50 rounded-lg">
          <h3 className="text-sm font-medium text-blue-300 mb-2">Status:</h3>
          <div className="text-xs text-gray-400 space-y-1">
            <p>Supported: {isSupported ? 'Yes' : 'No'}</p>
            <p>Recording: {isRecording ? 'Yes' : 'No'}</p>
            <p>Transcribing: {isTranscribing ? 'Yes' : 'No'}</p>
            <p>Has Error: {hasError ? 'Yes' : 'No'}</p>
            <p>Transcript: {transcript || 'None'}</p>
          </div>
        </div>

        {/* Mic Button Test */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-blue-300 mb-4">Microphone Test:</h3>
          <div className="flex items-center justify-center">
            <MicButton
              isListening={isRecording}
              isSupported={isSupported}
              hasError={hasError}
              onClick={toggleRecording}
            />
          </div>
        </div>

        {/* Recording/Transcribing Status */}
        {(isRecording || isTranscribing) && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-blue-300 mb-2">Status:</h3>
            <div className="text-sm text-blue-400 italic">
              {isRecording ? 'Recording...' : 'Transcribing...'}
            </div>
          </div>
        )}

        {/* Transcript Display */}
        {transcript && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-blue-300 mb-2">Transcript:</h3>
            <div className="p-3 bg-green-500/20 border border-green-500/50 rounded-lg">
              <p className="text-sm text-green-300">{transcript}</p>
              <button
                onClick={clearTranscript}
                className="mt-2 text-green-400 hover:text-green-300 text-xs"
              >
                Clear transcript
              </button>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-blue-300 mb-2">Error:</h3>
            <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg">
              <div className="flex items-center justify-between">
                <p className="text-sm text-red-300">{error}</p>
                <button
                  onClick={clearError}
                  className="text-red-400 hover:text-red-300 ml-4"
                >
                  ×
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="mt-8 p-4 bg-slate-700/50 rounded-lg">
          <h3 className="text-sm font-medium text-blue-300 mb-2">Test Instructions:</h3>
          <ol className="text-xs text-gray-400 space-y-1">
            <li>1. Click the microphone button to start recording</li>
            <li>2. Speak clearly into your microphone</li>
            <li>3. Click again to stop recording</li>
            <li>4. Wait for transcription to complete</li>
            <li>5. Check transcript appears below</li>
            <li>6. Requires backend endpoint: POST /api/transcribe</li>
          </ol>
        </div>
      </motion.div>
    </div>
  );
};

export default AudioRecorderTest;
