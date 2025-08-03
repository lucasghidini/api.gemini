import google.generativeai as genai
from typing import Optional, Union
from config import settings

class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def generate_response(self, prompt: str, context: Optional[str] = None, conversation_history: Optional[str] = None, image_data: Optional[bytes] = None) -> str:
        try:
            prompt_parts: list[Union[str,dict]] = []
            
            system_and_history = self._build_relationship_prompt(prompt,context,conversation_history)
            prompt_parts.append(system_and_history)

            if image_data:
                prompt_parts.append({
                    'mime_type': 'image/png',
                    'data': image_data
                                    })
                 
            response = self.model.generate_content(prompt_parts)
                
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return 'Não foi possível gerar uma resposta. Tente novamente.'

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
        - Análise de prints de conversas entre as pessoas
        
        
        Responda de forma informal,safada,direta, prática e construtiva.
        """
        
        prompt_parts = [system_prompt]
        
        if conversation_history:
            prompt_parts.append(f"\n\nHistórico da conversa:\n{conversation_history}")
        
        if context:
            prompt_parts.append(f"\n\nContexto adicional: {context}")
            
        prompt_parts.append(f"\n\nPergunta atual do usuário: {user_message}")
        
        return "".join(prompt_parts)