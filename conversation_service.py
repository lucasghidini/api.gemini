import uuid
from typing import Dict, List, Optional
from datetime import datetime
from models import Message, MessageType

class ConversationService:
    def __init__(self):
        self.conversations: Dict[str, List[Message]] = {}
    
    def create_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = []
        return conversation_id
    
    def get_conversation(self, conversation_id: str) -> Optional[List[Message]]:
        return self.conversations.get(conversation_id)
    
    def add_message(self, conversation_id: str, role: str, content: str, message_type: MessageType = MessageType.GENERAL) -> Message:
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        message = Message(
            role=role,
            content=content,
            message_type=message_type,
            timestamp=datetime.now()
        )
        
        self.conversations[conversation_id].append(message)
        return message
    
    def get_conversation_context(self, conversation_id: str, limit: Optional[int] = None) -> str:
        messages = self.get_conversation(conversation_id)
        if not messages:
            return ""
        
        if limit:
            messages = messages[-limit:]
        
        context_parts = []
        for msg in messages:
            role_label = "Usuário" if msg.role == "user" else "Assistente"
            context_parts.append(f"{role_label}: {msg.content}")
        
        return "\n".join(context_parts)
    
    def conversation_exists(self, conversation_id: str) -> bool:
        return conversation_id in self.conversations
    
    def delete_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False