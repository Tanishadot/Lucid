export type MessageRole = 'user' | 'assistant';

export interface Message {
  id: string;
  conversation_id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationWithMessages extends Conversation {
  messages: Message[];
}

export interface CreateConversationRequest {
  user_id: string;
  title: string;
}

export interface CreateMessageRequest {
  conversation_id: string;
  role: MessageRole;
  content: string;
}
