from typing import List, Dict

class PromptManager:
    """
    Centraliza la gestión de Prompts para evitar 'Magic Strings' en el código.
    """
    
    SYSTEM_PROMPT_TEMPLATE = (
        "Eres un asistente de IA experto y conciso desarrollado para una API técnica. "
        "Tu objetivo es responder preguntas con precisión técnica. "
        "Hoy es {current_date}. "
        "Contexto del usuario: {user_context}"
    )

    @staticmethod
    def build_messages(user_message: str, history: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """Construye la lista de mensajes para el LLM, incluyendo historial."""
        messages = []
        
        # System Prompt (Aquí podrías inyectar fechas dinámicas, contexto de usuario, etc.)
        messages.append({
            "role": "system", 
            "content": PromptManager.SYSTEM_PROMPT_TEMPLATE.format(
                current_date="31 de Diciembre, 2025",
                user_context="Usuario invitado"
            )
        })

        # Historial de chat (para mantener contexto)
        if history:
            messages.extend(history)

        # Mensaje actual
        messages.append({"role": "user", "content": user_message})
        
        return messages