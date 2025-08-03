from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models import ConversationResponse, Message, MessageType
from gemini_service import GeminiService
from conversation_service import ConversationService
from config import settings
import uvicorn




app = FastAPI(
    title="Assistente de Relacionamentos",
    description="API para assistência em comunicação e relacionamentos com histórico persistido",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_service = GeminiService()
conversation_service = ConversationService()

@app.get("/")
async def root():
    return {"message": "Assistente de Relacionamentos API v2.0 - Online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "relationship-assistant", "version": "2.0.0"}

@app.post("/conversation", response_model=ConversationResponse)
async def handle_conversation(
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    context: Optional[str] = Form(None),
    message_type: MessageType = Form(MessageType.GENERAL),
    image_file: Optional[UploadFile] = File(None)
                            ): # Alterando como a função recebe os dados agora recebe campo individualmente, usando form para textos e file para imagens
    try:
        
        if not conversation_id:
            conversation_id = conversation_service.create_conversation()
        elif not conversation_service.conversation_exists(conversation_id):
            raise HTTPException(status_code=404, detail="Conversa não encontrada")
        
        image_data = None
        if image_file:
            image_data = await image_file.read()
        
        conversation_service.add_message(
            conversation_id, 
            "user", 
            message, 
            message_type
        )
        
        conversation_history = conversation_service.get_conversation_context(conversation_id, limit=10)
        
        response_text = await gemini_service.generate_response(
            prompt=message,
            context=context,
            conversation_history=conversation_history
        )
        
        conversation_service.add_message(
            conversation_id,
            "assistant", 
            response_text,
            message_type
        )
        
        history = conversation_service.get_conversation(conversation_id)
        
        return ConversationResponse(
            conversation_id=conversation_id,
            response=response_text,
            message_type= message_type,
            history=history or []
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug
    )