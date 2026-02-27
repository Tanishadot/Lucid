import axios from 'axios';

// Test backend connectivity
const testBackend = async () => {
  try {
    console.log('Testing backend connection...');
    
    // Test health endpoint
    const healthResponse = await axios.get('http://localhost:8000/health');
    console.log('Health check:', healthResponse.data);
    
    // Test transcription endpoint with a mock file
    const mockBlob = new Blob(['mock audio data'], { type: 'audio/webm' });
    const formData = new FormData();
    formData.append('file', mockBlob, 'test.webm');
    
    const transcribeResponse = await axios.post('http://localhost:8000/api/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 5000,
    });
    
    console.log('Transcription test:', transcribeResponse.data);
    
  } catch (error) {
    console.error('Backend test failed:', error);
    if (axios.isAxiosError(error)) {
      console.error('Error details:', {
        message: error.message,
        code: error.code,
        status: error.response?.status,
        statusText: error.response?.statusText,
      });
    }
  }
};

// Run test
testBackend();
