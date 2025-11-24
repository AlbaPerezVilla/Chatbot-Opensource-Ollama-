from typing import Optional, Dict, Any, List
import ollama

from experts.expert_prompts import ExpertType
from core.conversation import ConversationManager


class ModelNotAvailableError(Exception):
    """Error cuando el modelo de Ollama no está disponible."""
    pass


class ConnectionErrorOllama(Exception):
    """Error cuando el servicio Ollama no responde."""
    pass


class ThematicChatbot:
    """
    Lógica principal del chatbot temático usando Ollama (gemma3:1b).
    Funciona completamente offline si Ollama y el modelo están disponibles localmente.
    """

    def __init__(self,
                 model_name: str = "gemma3:1b",
                 initial_expert: ExpertType = ExpertType.PROGRAMMING) -> None:
        # IMPORTANTE: primero guardamos el nombre del modelo
        self.model_name = model_name

        # IMPORTANTE: creamos el gestor de conversación
        self.conversation_manager = ConversationManager(initial_expert)

        # Comprobación inicial: ¿está disponible el modelo?
        self._check_model_available()

    def _check_model_available(self) -> None:
        """
        Verifica que el modelo esté disponible en el servidor local de Ollama.
        Lanza ModelNotAvailableError si no se encuentra.
        """
        try:
            # Lista de modelos instalados
            response = ollama.list()
            models = [m.get("model") or m.get("name") for m in response.get("models", [])]

            if self.model_name not in models:
                raise ModelNotAvailableError(
                    f"El modelo '{self.model_name}' no está disponible en Ollama.\n"
                    f"Instálalo con: ollama pull {self.model_name} en la terminal de windows"
                )
        except Exception as e:
            # Si ni siquiera responde ollama.list(), probablemente no está corriendo el servicio
            raise ConnectionErrorOllama(
                "No se pudo conectar con el servidor local de Ollama. "
                "Asegúrate de que Ollama está instalado y en ejecución."
            ) from e

    def set_expert(self, expert: ExpertType, reset_history: bool = False) -> None:
        """Cambia el experto activo y gestiona el historial según la opción."""
        self.conversation_manager.set_expert(expert, reset_history=reset_history)

    def get_active_expert(self) -> ExpertType:
        return self.conversation_manager.get_current_expert()

    def get_history(self) -> List[Dict[str, str]]:
        return self.conversation_manager.get_history()

    def send_message(self, user_message: str) -> str:
        """
        Envía un mensaje del usuario al modelo gemma3:1b con el contexto del experto activo.
        Devuelve el texto de la respuesta del modelo.
        """
        # Añadir mensaje de usuario al historial
        self.conversation_manager.add_user_message(user_message)
        history = self.conversation_manager.get_history()

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=history,
                stream=False  # para simplificar; se podría usar stream=True
            )
        except Exception as e:
            raise ConnectionErrorOllama(
                "Error al comunicarse con Ollama durante la generación de la respuesta."
            ) from e

        # El formato típico: {"message": {"role": "assistant", "content": "..."}}
        assistant_message = response.get("message", {}).get("content", "")

        # Guardar respuesta en el historial
        self.conversation_manager.add_assistant_message(assistant_message)

        return assistant_message
