from fastapi import HTTPException

class GeminiServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ConfigurationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def handle_service_errors(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except GeminiServiceError as e:
            raise HTTPException(status_code=503, detail=f"Erro no serviço Gemini: {e.message}")
        except ConfigurationError as e:
            raise HTTPException(status_code=500, detail=f"Erro de configuração: {e.message}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    return wrapper