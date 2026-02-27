import { useState, useRef, useCallback } from 'react';
import axios from 'axios';

interface TranscriptionResponse {
  transcript: string;
}

export const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isSupported, setIsSupported] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  // Check if MediaRecorder is supported
  useState(() => {
    const supported = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && MediaRecorder);
    setIsSupported(supported);
    if (!supported) {
      setError('Audio recording not supported in this browser');
      setHasError(true);
    }
  });

  const startRecording = useCallback(async () => {
    if (!isSupported) {
      setError('Audio recording not supported in this browser');
      setHasError(true);
      return;
    }

    try {
      // Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Clear previous chunks
      chunksRef.current = [];
      
      // Create MediaRecorder
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      // Handle data available
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      // Handle recording stop
      mediaRecorder.onstop = async () => {
        setIsRecording(false);
        
        // Combine chunks into blob
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
        
        // Transcribe the audio
        await transcribeAudio(audioBlob);
      };

      // Handle recording error
      mediaRecorder.onerror = (event) => {
        console.error('MediaRecorder error:', event);
        setIsRecording(false);
        setHasError(true);
        setError('Recording failed');
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      // Start recording
      mediaRecorder.start();
      setIsRecording(true);
      setError(null);
      setHasError(false);
      
    } catch (err) {
      console.error('Failed to start recording:', err);
      setIsRecording(false);
      setHasError(true);
      
      if (err instanceof Error) {
        if (err.name === 'NotAllowedError') {
          setError('Microphone permission denied');
        } else if (err.name === 'NotFoundError') {
          setError('No microphone found');
        } else {
          setError('Unable to access microphone');
        }
      } else {
        setError('Unable to access microphone');
      }
    }
  }, [isSupported]);

  const transcribeAudio = useCallback(async (audioBlob: Blob) => {
    setIsTranscribing(true);
    
    try {
      // Create form data
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');
      
      // Send to backend
      const response = await axios.post<TranscriptionResponse>('http://localhost:8000/api/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      });
      
      console.log('Transcription response:', response.data);
      
      // Set transcript
      setTranscript(response.data.transcript);
      setError(null);
      setHasError(false);
      
    } catch (err) {
      console.error('Transcription failed:', err);
      setHasError(true);
      
      if (axios.isAxiosError(err)) {
        if (err.code === 'ECONNABORTED') {
          setError('Transcription timed out');
        } else if (err.response?.status === 413) {
          setError('Audio file too large');
        } else if (err.response?.status >= 500) {
          setError('Transcription service unavailable');
        } else {
          setError('Transcription failed');
        }
      } else {
        setError('Transcription failed');
      }
    } finally {
      setIsTranscribing(false);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
    }
  }, [isRecording]);

  const toggleRecording = useCallback(() => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  }, [isRecording, startRecording, stopRecording]);

  const clearError = useCallback(() => {
    setError(null);
    setHasError(false);
  }, []);

  const clearTranscript = useCallback(() => {
    setTranscript('');
  }, []);

  return {
    isRecording,
    transcript,
    isSupported,
    hasError,
    error,
    isTranscribing,
    startRecording,
    stopRecording,
    toggleRecording,
    clearError,
    clearTranscript,
  };
};
