from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class MessageType(str, Enum):
    ADVICE = "advice"
    MESSAGE_SUGGESTION = "message_suggestion"
    CONVERSATION_ANALYSIS = "conversation_analysis"
    GENERAL = "general"

class Message(BaseModel):
    role: str = Field(..., description="Papel da mensagem: 'user' ou 'assistant'")
    content: str = Field(..., description="Conteúdo da mensagem")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da mensagem")
    message_type: MessageType = Field(MessageType.GENERAL, description="Tipo da mensagem")

class ConversationRequest(BaseModel):
    conversation_id: Optional[str] = Field(None, description="ID da conversa existente")
    message: str = Field(..., description="Nova mensagem do usuário")
    message_type: MessageType = Field(MessageType.GENERAL, description="Tipo de solicitação")
    context: Optional[str] = Field(None, description="Contexto adicional específico para esta mensagem")

class ConversationResponse(BaseModel):
    conversation_id: str = Field(..., description="ID da conversa")
    response: str = Field(..., description="Resposta do assistente")
    message_type: MessageType = Field(..., description="Tipo da resposta")
    history: List[Message] = Field(..., description="Histórico completo da conversa")