from typing import List
from langchain_core.messages import BaseMessage

# Simple in-memory conversation store per session
conversation_memory = {}

def get_memory(session_id: str) -> List[BaseMessage]:
    return conversation_memory.get(session_id, [])

def add_to_memory(session_id: str, message: BaseMessage):
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    conversation_memory[session_id].append(message)