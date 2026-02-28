import React, { useState, useEffect } from 'react';
import { MessageSquare, Plus, Trash2, Loader2 } from 'lucide-react';
import { conversationApi } from '../services/conversationApi';
import { Conversation } from '../types/conversation';

interface ConversationSidebarProps {
  activeConversationId: string | null;
  onConversationSelect: (conversationId: string) => void;
  onNewConversation: () => void;
  className?: string;
}

const ConversationSidebar: React.FC<ConversationSidebarProps> = ({
  activeConversationId,
  onConversationSelect,
  onNewConversation,
  className = ''
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchConversations = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await conversationApi.getConversations();
      setConversations(data);
    } catch (err) {
      setError('Failed to load conversations');
      console.error('Error fetching conversations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteConversation = async (e: React.MouseEvent, conversationId: string) => {
    e.stopPropagation(); // Prevent conversation selection
    
    try {
      setDeletingId(conversationId);
      await conversationApi.deleteConversation(conversationId);
      
      // Remove from local state
      setConversations(prev => prev.filter(conv => conv.id !== conversationId));
      
      // If this was the active conversation, trigger new conversation
      if (conversationId === activeConversationId) {
        onNewConversation();
      }
    } catch (err) {
      console.error('Error deleting conversation:', err);
      // You could show a toast notification here
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  return (
    <div className={`bg-gray-900 border-r border-gray-800 flex flex-col ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-800">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <MessageSquare size={20} />
            Conversations
          </h2>
          <button
            onClick={onNewConversation}
            className="p-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition-colors"
            title="New conversation"
          >
            <Plus size={16} />
          </button>
        </div>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="animate-spin text-gray-400" size={24} />
          </div>
        ) : error ? (
          <div className="p-4 text-center">
            <p className="text-red-400 text-sm">{error}</p>
            <button
              onClick={fetchConversations}
              className="mt-2 text-blue-400 hover:text-blue-300 text-sm"
            >
              Retry
            </button>
          </div>
        ) : conversations.length === 0 ? (
          <div className="p-4 text-center">
            <p className="text-gray-400 text-sm">No conversations yet</p>
            <p className="text-gray-500 text-xs mt-1">Start a new conversation to begin</p>
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {conversations.map((conversation) => (
              <div
                key={conversation.id}
                onClick={() => onConversationSelect(conversation.id)}
                className={`group relative p-3 rounded-lg cursor-pointer transition-colors ${
                  activeConversationId === conversation.id
                    ? 'bg-blue-900/30 border border-blue-700/50'
                    : 'hover:bg-gray-800 border border-transparent'
                }`}
              >
                <div className="pr-8">
                  <h3 className="text-white text-sm font-medium truncate">
                    {conversation.title}
                  </h3>
                  <p className="text-gray-400 text-xs mt-1">
                    {formatDate(conversation.updated_at)}
                  </p>
                </div>
                
                {/* Delete button */}
                <button
                  onClick={(e) => handleDeleteConversation(e, conversation.id)}
                  disabled={deletingId === conversation.id}
                  className="absolute top-3 right-3 p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity bg-red-600/80 hover:bg-red-600 text-white"
                  title="Delete conversation"
                >
                  {deletingId === conversation.id ? (
                    <Loader2 size={14} className="animate-spin" />
                  ) : (
                    <Trash2 size={14} />
                  )}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationSidebar;
