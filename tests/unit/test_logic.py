from app.services.prompt_manager import PromptManager

def test_build_messages_structure():
    """Verifica que se agregue el System Prompt y el mensaje del usuario."""
    msg = "Hola mundo"
    messages = PromptManager.build_messages(msg)
    
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "2025" in messages[0]["content"] # Verifica fecha inyectada
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "Hola mundo"

def test_build_messages_with_history():
    """Verifica que el historial se inyecte en el orden correcto."""
    history = [
        {"role": "user", "content": "Pregunta 1"},
        {"role": "assistant", "content": "Respuesta 1"}
    ]
    msg = "Pregunta 2"
    messages = PromptManager.build_messages(msg, history)
    
    # System + 2 historia + 1 actual = 4
    assert len(messages) == 4
    assert messages[1]["content"] == "Pregunta 1"
    assert messages[3]["content"] == "Pregunta 2"