from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="El mensaje del usuario")
    history: Optional[List[Message]] = Field(default=[], description="Historial de conversación previo")
    stream: bool = Field(default=False, description="Si es True, devuelve una respuesta en streaming")

class ChatResponse(BaseModel):
    response: str
    model_used: str