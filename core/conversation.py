# core/conversation.py

from typing import List, Dict, Any
from experts.expert_prompts import ExpertType, get_system_prompt_for_expert

class ConversationManager:
    """
    Gestiona el historial de conversación por experto y el experto activo.
    """

    def __init__(self, initial_expert: ExpertType):
        # Historial separado por experto
        self.histories: Dict[ExpertType, List[Dict[str, str]]] = {
            expert: [] for expert in ExpertType
        }
        self.current_expert: ExpertType = initial_expert

        # Inicializa cada historial con el mensaje de sistema correspondiente
        for expert in ExpertType:
            system_prompt = get_system_prompt_for_expert(expert)
            self.histories[expert].append({
                "role": "system",
                "content": system_prompt
            })

    def set_expert(self, expert: ExpertType, reset_history: bool = False) -> None:
        """
        Cambia el experto activo.
        Si reset_history es True, reinicia el historial de ese experto
        manteniendo solo el mensaje de sistema.
        """
        self.current_expert = expert

        if reset_history:
            system_prompt = get_system_prompt_for_expert(expert)
            self.histories[expert] = [{
                "role": "system",
                "content": system_prompt
            }]

    def get_current_expert(self) -> ExpertType:
        return self.current_expert

    def get_history(self, expert: ExpertType | None = None) -> List[Dict[str, str]]:
        """Devuelve el historial del experto indicado o del actual."""
        if expert is None:
            expert = self.current_expert
        return self.histories[expert]

    def add_user_message(self, content: str, expert: ExpertType | None = None) -> None:
        """Añade un mensaje de usuario al historial del experto indicado o del actual."""
        if expert is None:
            expert = self.current_expert
        self.histories[expert].append({
            "role": "user",
            "content": content
        })

    def add_assistant_message(self, content: str, expert: ExpertType | None = None) -> None:
        """Añade un mensaje de asistente al historial del experto indicado o del actual."""
        if expert is None:
            expert = self.current_expert
        self.histories[expert].append({
            "role": "assistant",
            "content": content
        })