import { create } from 'zustand';

interface Session {
  id: string;
  messages: Array<{
    id: string;
    text: string;
    isUser: boolean;
    timestamp: Date;
  }>;
}

interface SessionStore {
  currentSession: Session | null;
  sessions: Session[];
  createSession: () => void;
  addMessage: (text: string, isUser: boolean) => void;
  clearSession: () => void;
}

export const useSessionStore = create<SessionStore>((set, get) => ({
  currentSession: null,
  sessions: [],

  createSession: () => {
    const newSession: Session = {
      id: Date.now().toString(),
      messages: [],
    };
    set({ currentSession: newSession });
  },

  addMessage: (text: string, isUser: boolean) => {
    const { currentSession } = get();
    if (!currentSession) return;

    const newMessage = {
      id: Date.now().toString(),
      text,
      isUser,
      timestamp: new Date(),
    };

    set(state => ({
      currentSession: state.currentSession
        ? {
            ...state.currentSession,
            messages: [...state.currentSession.messages, newMessage],
          }
        : null,
    }));
  },

  clearSession: () => {
    set({ currentSession: null });
  },
}));
