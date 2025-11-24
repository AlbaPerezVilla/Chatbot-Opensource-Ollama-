# main.py

from experts.expert_prompts import ExpertType
from core.chatbot import ThematicChatbot, ModelNotAvailableError, ConnectionErrorOllama 

def show_main_menu(active_expert: ExpertType) -> None:
    print("\n" + "=" * 60)
    print("CHATBOT DE EXPERTOS TEMÁTICOS (gemma3:1b - offline)")
    print("=" * 60)
    print(f"Experto activo: {expert_human_name(active_expert)}\n")
    print("Opciones:")
    print("  1 - Cambiar de experto")
    print("  2 - Reiniciar historial del experto actual")
    print("  3 - Empezar / continuar conversación con el experto activo")
    print("  0 - Salir")
    print("=" * 60)

def expert_human_name(expert: ExpertType) -> str:
    if expert == ExpertType.PROGRAMMING:
        return "Programador de Software"
    if expert == ExpertType.MARKETING:
        return "Experto Marketing"
    if expert == ExpertType.LEGAL:
        return "Experto Jurídico-Legal"
    return str(expert)

def choose_expert_menu() -> ExpertType | None:
    print("\n Selecciona el experto:")
    print("  1 - Programador de Software")
    print("  2 - Experto Marketing")
    print("  3 - Experto Jurídico-Legal")
    print("  0 - Cancelar")
    choice = input("Opción: ").strip()

    if choice == "1":
        return ExpertType.PROGRAMMING
    elif choice == "2":
        return ExpertType.MARKETING
    elif choice == "3":
        return ExpertType.LEGAL
    elif choice == "0":
        return None
    else:
        print("Opción no válida.")
        return None

def conversation_loop(chatbot: ThematicChatbot) -> None:
    """
    Bucle de conversación para el experto activo.
    Permite múltiples intercambios y volver al menú principal.
    """
    print("\nEntrando en el modo conversación.")
    print("Escribe tu petición para el experto.")
    print("Comandos especiales:")
    print("  /menu   - Volver al menú principal")
    print("  /expert - Cambiar de experto")
    print("  /reset  - Reiniciar historial del experto actual")
    print("  /salir  - Salir del programa\n")

    while True:
        active_expert = chatbot.get_active_expert()
        user_input = input(f"[Tú -> {expert_human_name(active_expert)}]: ").strip()

        if not user_input:
            continue

        # Comandos especiales
        if user_input.lower() == "/menu":
            print("Volviendo al menú principal...")
            break
        if user_input.lower() == "/salir":
            print("Saliendo del programa. Muchas gracias, adiós!")
            raise SystemExit(0)
        if user_input.lower() == "/reset":
            chatbot.set_expert(active_expert, reset_history=True)
            print("Historial del experto actual reiniciado.")
            continue
        if user_input.lower() == "/expert":
            new_expert = choose_expert_menu()
            if new_expert is not None:
                # Por defecto, mantenemos historial al cambiar de experto
                chatbot.set_expert(new_expert, reset_history=False)
                print(f"Experto cambiado a: {expert_human_name(new_expert)}")
            continue

        # Mensaje normal -> enviamos al modelo
        try:
            response = chatbot.send_message(user_input)
            print(f"[{expert_human_name(active_expert)}]: {response}\n")
        except ConnectionErrorOllama as e:
            print(f"\n[ERROR DE CONEXIÓN] {e}")
            print("Regresando al menú principal...\n")
            break
        except Exception as e:
            print(f"\n[ERROR DESCONOCIDO] {e}")
            print("Regresando al menú principal...\n")
            break

def main():
    print("=" * 60)
    print(" INICIALIZANDO CHATBOT DE EXPERTOS (gemma3:1b - offline)")
    print("=" * 60)

    try:
        chatbot = ThematicChatbot(model_name="gemma3:1b",
                                  initial_expert=ExpertType.PROGRAMMING)
    except ModelNotAvailableError as e:
        print("\n[ERROR] Modelo no disponible:")
        print(e)
        return
    except ConnectionErrorOllama as e:
        print("\n[ERROR] No se pudo conectar a Ollama:")
        print(e)
        return
    except Exception as e:
        print("\n[ERROR] Fallo inesperado al inicializar el chatbot:")
        print(e)
        return

    # Bucle principal de la aplicación
    while True:
        active_expert = chatbot.get_active_expert()
        show_main_menu(active_expert)
        option = input("Selecciona una opción: ").strip()

        if option == "0":
            print("Saliendo del programa. Muchas gracias, adiós!")
            break

        elif option == "1":
            new_expert = choose_expert_menu()
            if new_expert is not None:
                # Preguntar si quiere reiniciar historial o mantener
                print("\n¿Quieres reiniciar el historial de ese experto?")
                print("  1 - Sí, reiniciar historial")
                print("  2 - No, mantener historial anterior")
                reset_choice = input("Opción: ").strip()
                reset = reset_choice == "1"
                chatbot.set_expert(new_expert, reset_history=reset)
                print(f"Experto activo ahora: {expert_human_name(new_expert)}")

        elif option == "2":
            active_expert = chatbot.get_active_expert()
            chatbot.set_expert(active_expert, reset_history=True)
            print("Historial del experto actual se ha reiniciado.")

        elif option == "3":
            conversation_loop(chatbot)

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()

