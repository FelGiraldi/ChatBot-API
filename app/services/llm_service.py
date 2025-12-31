import logging
from groq import AsyncGroq
from app.core.config import get_settings
from app.services.prompt_manager import PromptManager
from typing import List, Dict, AsyncGenerator

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncGroq(api_key=self.settings.GROQ_API_KEY)
    
    async def generate_response(self, message: str, history: List[Dict[str, str]] = None) -> str:
        """
        Genera una respuesta completa (no-streaming).
        Maneja errores de la API externa aquí para no ensuciar el router.
        """
        try:
            messages = PromptManager.build_messages(message, history)
            
            chat_completion = await self.client.chat.completions.create(
                messages=messages,
                model=self.settings.DEFAULT_MODEL,
                temperature=0.5,
                max_tokens=1024,
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error en LLMService: {str(e)}")
            # En un entorno real, aquí lanzaríamos una CustomException definida en core/exceptions.py
            raise e

    async def stream_response(self, message: str, history: List[Dict[str, str]] = None) -> AsyncGenerator[str, None]:
        """
        Generador asíncrono para Streaming (Server-Sent Events).
        Demuestra capacidad Senior de manejar latencia.
        """
        messages = PromptManager.build_messages(message, history)
        
        stream = await self.client.chat.completions.create(
            messages=messages,
            model=self.settings.DEFAULT_MODEL,
            temperature=0.5,
            max_tokens=1024,
            stream=True,
        )
        
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content