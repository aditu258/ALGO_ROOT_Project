from datetime import datetime
from typing import Dict, List

class SessionManager:
    """
    Remembers user interactions to enable conversational AI
    Stores: timestamp, user request, and executed function
    """
    def __init__(self):
        self.sessions: Dict[str, List[dict]] = {}  # Stores all conversations

    def add_to_session(self, session_id: str, prompt: str, function_name: str):
        """Records each user interaction for context"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []  # Start new conversation
            
        self.sessions[session_id].append({
            "timestamp": datetime.now().isoformat(),  # When it happened
            "prompt": prompt,  # What the user asked
            "function": function_name  # What we did
        })

    def get_session_context(self, session_id: str) -> List[dict]:
        """Retrieves full conversation history"""
        return self.sessions.get(session_id, [])