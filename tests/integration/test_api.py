import pytest
from unittest.mock import AsyncMock
from app.api.v1.endpoints.chat import get_llm_service
from app.main import app
from app.services.llm_service import LLMService

# 1. Creamos el Mock del servicio
mock_llm_service = AsyncMock(spec=LLMService)

# Definimos qué debe responder el mock
async def mock_generate_response(message, history=None):
    return "Esta es una respuesta simulada por test."

async def mock_stream_response(message, history=None):
    # Simulamos generador asíncrono
    chunks = ["Chunk 1", " ", "Chunk 2"]
    for chunk in chunks:
        yield chunk

# Asignamos los comportamientos al mock
mock_llm_service.generate_response.side_effect = mock_generate_response
mock_llm_service.stream_response.side_effect = mock_stream_response

# 2. Override de la dependencia en FastAPI
app.dependency_overrides[get_llm_service] = lambda: mock_llm_service

@pytest.mark.asyncio
async def test_chat_endpoint_standard(async_client):
    """Prueba flujo normal JSON sin llamar a Groq real."""
    payload = {
        "message": "Hola test",
        "stream": False
    }
    
    response = await async_client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Esta es una respuesta simulada por test."
    assert "model_used" in data

@pytest.mark.asyncio
async def test_chat_endpoint_streaming(async_client):
    """Prueba flujo streaming."""
    payload = {
        "message": "Hola stream",
        "stream": True
    }
    
    async with async_client.stream("POST", "/api/v1/chat", json=payload) as response:
        assert response.status_code == 200
        # Leemos el stream completo
        body = [chunk async for chunk in response.aiter_text()]
        full_text = "".join(body)
        
    assert "Chunk 1 Chunk 2" in full_text

@pytest.mark.asyncio
async def test_validation_error(async_client):
    """Prueba que Pydantic rechace mensajes vacíos."""
    payload = {"message": ""} # Vacío intencional
    
    response = await async_client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 422 # Unprocessable Entity