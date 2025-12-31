from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import chat
from app.core.config import get_settings
from app.core.exceptions import LLMProviderError

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="API demostrativa de integración LLM End-to-End"
)

# Global Exception Handler
@app.exception_handler(LLMProviderError)
async def llm_exception_handler(request: Request, exc: LLMProviderError):
    return JSONResponse(
        status_code=503,
        content={"detail": "El servicio de IA no está disponible momentáneamente. Intente más tarde."},
    )

# Router registration
app.include_router(chat.router, prefix=settings.API_V1_STR)