from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.models.chat import ChatResponse
from pydantic import BaseModel

router = APIRouter()

# Schema simple para input
class UserMessageRequest(BaseModel):
    message: str

class ConversationResponse(BaseModel):
    id: int
    created_at: str

@router.post("/conversations", response_model=ConversationResponse)
async def start_conversation(
    db: AsyncSession = Depends(get_db)
):
    """Inicia una nueva conversación vacía y devuelve su ID."""
    llm = LLMService()
    service = ChatService(db, llm)
    new_chat = await service.create_conversation()
    return {"id": new_chat.id, "created_at": str(new_chat.created_at)}

@router.post("/conversations/{conversation_id}/messages", response_model=ChatResponse)
async def send_message(
    request: UserMessageRequest,
    conversation_id: int = Path(..., title="ID de la conversación"),
    db: AsyncSession = Depends(get_db)
):
    """
    Envía un mensaje a una conversación específica.
    La API recupera el historial automáticamente de la BD.
    """
    llm = LLMService()
    service = ChatService(db, llm)
    
    try:
        return await service.process_user_message(conversation_id, request.message)
    except Exception as e:
        # Aquí deberías manejar si el ID no existe
        raise HTTPException(status_code=500, detail=str(e))