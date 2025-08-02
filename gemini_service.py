import google.generativeai as genai
from typing import Optional
from config import settings

class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def generate_response(self, prompt: str, context: Optional[str] = None, conversation_history: Optional[str] = None) -> str:
        try:
            full_prompt = self._build_relationship_prompt(prompt, context, conversation_history)
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta do Gemini: {str(e)}")
    
    def _build_relationship_prompt(self, user_message: str, context: Optional[str] = None, conversation_history: Optional[str] = None) -> str:
        system_prompt = """
        Você é um assistente especialista em relacionamentos e comunicação interpessoal para homens.
        Seu objetivo é fornecer conselhos respeitosos, genuínos e éticos sobre:
        
        - Comunicação eficaz com mulheres
        - Desenvolvimento de confiança e carisma
        - Sugestões de mensagens respeitosas
        - Análise de conversas
        - Técnicas de flerte saudável
        - Construção de relacionamentos autênticos
        
        
        Responda de forma informal,safada,direta, prática e construtiva.
        """
        
        prompt_parts = [system_prompt]
        
        if conversation_history:
            prompt_parts.append(f"\n\nHistórico da conversa:\n{conversation_history}")
        
        if context:
            prompt_parts.append(f"\n\nContexto adicional: {context}")
            
        prompt_parts.append(f"\n\nPergunta atual do usuário: {user_message}")
        
        return "".join(prompt_parts)