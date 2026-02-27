conversation_memory = []

def store_interaction(user_input, response):
    conversation_memory.append({"user": user_input, "assistant": response})

def get_memory():
    return conversation_memory[-5:]

def get_context_for_embedding():
    """Get conversation context for embedding"""
    recent_turns = conversation_memory[-3:] if conversation_memory else []
    context = "\n".join([
        f"User: {turn['user']}\nAssistant: {turn['assistant']}" 
        for turn in recent_turns
    ])
    return context