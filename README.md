# Chatbot de Expertos Temáticos con Ollama (gemma3:1b)

Este proyecto implementa un chatbot de consola que permite conversar con tres expertos temáticos distintos utilizando el modelo local `gemma3:1b`
a través de Ollama. El programa funciona completamente offline siempre que Ollama y el modelo estén instalados en la máquina.

## Expertos disponibles

- **Programación de Software**
- **Marketing**
- **Jurídico-Legal** (orientación general, no asesoría profesional)

## Requisitos previos

1. Tener instalado **Python 3.10+** (o similar).
2. Tener instalado **Ollama** y corriendo el servicio local.
3. Descargar el modelo `gemma3:1b`:

En el terminal de Windows, indicar lo siguiente:

```bash
ollama pull gemma3:1b

# En la terminal de VS CODE

# 1. Ir al directorio del proyecto
cd "C:\Users\albap\OneDrive\Escritorio\Bootcamp IA\SPRINT 4\LAB 2\chatbot_opensource"

# 2. Activar el entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Instalar las dependencias
pip install -r requirements.txt
# (Si la librería ollama no se instalara correctamente)
# pip install ollama

# 4. Ejecutar el chatbot
python main.py