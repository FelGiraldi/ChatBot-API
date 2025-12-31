from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sql_models import Conversation, Message
from app.models.chat import ChatResponse
from app.services.llm_service import LLMService

class ChatService:
    def __init__(self, db: AsyncSession, llm: LLMService):
        self.db = db
        self.llm = llm

    async def create_conversation(self) -> Conversation:
        """Crea una nueva sesión de chat vacía"""
        new_chat = Conversation()
        self.db.add(new_chat)
        await self.db.commit()
        await self.db.refresh(new_chat)
        return new_chat

    async def get_conversation_history(self, conversation_id: int):
        """Recupera mensajes anteriores ordenados por fecha"""
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()

    async def process_user_message(self, conversation_id: int, user_message: str) -> ChatResponse:
        """Procesa el mensaje del usuario, llama al LLM y guarda la respuesta"""
        
        # 1. Guardar mensaje del usuario en DB
        user_msg_db = Message(conversation_id=conversation_id, role="user", content=user_message)
        self.db.add(user_msg_db)
        # Commit parcial para que el mensaje ya sea parte de la historia si falla el LLM
        await self.db.commit() 

        # 2. Recuperar historial completo para contexto
        history_objs = await self.get_conversation_history(conversation_id)
        
        # Convertir objetos SQLAlchemy a lista de dicts para el LLM
        history_dicts = [{"role": m.role, "content": m.content} for m in history_objs]

        # 3. Llamar al LLM (Nota: Aquí estamos enviando el historial completo incluyendo el actual)
        # Ajuste: el prompt manager espera el mensaje actual separado o incluido. 
        ai_response_text = await self.llm.generate_response(
            message=user_message, 
            history=history_dicts[:-1] # Excluir el mensaje actual que acabamos de guardar
        )

        # 4. Guardar respuesta de IA en DB
        ai_msg_db = Message(conversation_id=conversation_id, role="assistant", content=ai_response_text)
        self.db.add(ai_msg_db)
        await self.db.commit()

        return ChatResponse(
            response=ai_response_text,
            model_used="llama-3.3-70b-versatile"
        )