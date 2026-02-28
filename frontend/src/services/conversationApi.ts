import axios from 'axios';
import {
  Conversation,
  ConversationWithMessages,
  CreateConversationRequest,
  CreateMessageRequest,
  Message
} from '../types/conversation';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Mock user ID - in production, this would come from authentication
const MOCK_USER_ID = '550e8400-e29b-41d4-a716-446655440000';

export const conversationApi = {
  // Get all conversations for the current user
  async getConversations(): Promise<Conversation[]> {
    try {
      const response = await api.get('/api/conversations');
      return response.data;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  },

  // Get a specific conversation with all messages
  async getConversation(conversationId: string): Promise<ConversationWithMessages> {
    try {
      const response = await api.get(`/api/conversations/${conversationId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching conversation:', error);
      throw error;
    }
  },

  // Create a new conversation
  async createConversation(title: string): Promise<Conversation> {
    try {
      const request: CreateConversationRequest = {
        user_id: MOCK_USER_ID,
        title
      };
      const response = await api.post('/api/conversations', request);
      return response.data;
    } catch (error) {
      console.error('Error creating conversation:', error);
      throw error;
    }
  },

  // Add a message to a conversation
  async addMessage(conversationId: string, role: 'user' | 'assistant', content: string): Promise<Message> {
    try {
      const request: CreateMessageRequest = {
        conversation_id: conversationId,
        role,
        content
      };
      const response = await api.post(`/api/conversations/${conversationId}/messages`, request);
      return response.data;
    } catch (error) {
      console.error('Error adding message:', error);
      throw error;
    }
  },

  // Delete a conversation
  async deleteConversation(conversationId: string): Promise<void> {
    try {
      await api.delete(`/api/conversations/${conversationId}`);
    } catch (error) {
      console.error('Error deleting conversation:', error);
      throw error;
    }
  },

  // Start a new conversation with the first message
  async startNewConversation(firstMessage: string): Promise<ConversationWithMessages> {
    try {
      const response = await api.post('/api/conversations/start', { first_message: firstMessage });
      return response.data;
    } catch (error) {
      console.error('Error starting new conversation:', error);
      throw error;
    }
  }
};
