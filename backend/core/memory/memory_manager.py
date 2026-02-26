conversation_memory = []

def store_interaction(user_input, response):
    conversation_memory.append({"user": user_input, "assistant": response})

def get_memory():
    return conversation_memory[-5:]