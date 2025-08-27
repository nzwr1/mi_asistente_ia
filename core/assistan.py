import sys
import os
import speech_recognition as sr
import pyttsx3 
import google.generativeai as genai
from dotenv import load_dotenv
import requests 
import json


# Cargar las variables del archivo .env
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configura la API con tu clave
genai.configure(api_key=GEMINI_API_KEY)

# Inicializa el modelo de Gemini
model = genai.GenerativeModel('models/gemini-2.5-pro')

# URL de tu agente local
AGENTE_URL = 'http://127.0.0.1:5000/ejecutar-comando'

# Inicializamos el reconocimiento de voz y texto
listener = sr.Recognizer()
engine = pyttsx3.init()

# Funcion para que el asistente hable
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Funcion para escuchar un comnado
def listen_command():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='es-ES')
            command = command.lower()
            if 'lilia' in command:
                command = command.replace('asistente', '')
                print(f"Comando recibido: {command}")
                return command.replace('lilia', '').strip()
    except sr.UnknownValueError:
        print("No te he entendido, por favor repite.")
        return "" 
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

# Función para procesar un comando con la IA
def process_command_and_check_json(command):
    """
    Envía el comando a Gemini, analiza la respuesta y, si es un JSON,
    lo envía al agente local.
    """
    try:
        #Pasa la instruccion a Gemini para que genere un JSON
        prompt = prompt = f"Eres un asistente de automatización que habla español. Si el usuario pide abrir un programa, responde SOLAMENTE con un objeto JSON con dos claves: 'accion' y 'nombre_programa'. El valor de 'accion' debe ser 'abrir_programa'. No incluyas ningún otro texto o formato. Por ejemplo, si el comando es 'abre Visual Studio Code', responde: {{'accion': 'abrir_programa', 'nombre_programa': 'vscode'}}. Si el usuario no pide abrir un programa, responde conversacionalmente. Comando: '{command}'"

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        print(f"Respuesta de Lilia: {response_text}")

        try:
            # Limpia la respuesta de Gemini eliminando los delimitadores de código
            if response_text.startswith('```json') and response_text.endswith('```'):
                response_text = response_text.strip('```json').strip('```').strip()

            # Intenta decodificar la respuesta como JSON
            comando_json = json.loads(response_text)

            # Si tienes exito, significa que es un comando para el agente
            print(f"La IA ha generado un comando JSON. Enviando al agente local...")

            # Envia la peticion POST al agente local
            response_agente = requests.post(AGENTE_URL, json=comando_json) 
            response_agente.raise_for_status()  # Lanza un error si la respuesta no es 200 OK

            # Imprime la respuesta del agente local y lo dice en voz alta
            agente_respuesta = response_agente.json().get('mensaje', 'No hay mensaje en la respuesta del agente.')
            print(f"Respuesta del agente local: {agente_respuesta}")
            speak(agente_respuesta)

        except json.JSONDecodeError:
            # Si el JSON falla, la respuesta es conversacional
            print("La IA ha respondido con un mensaje conversacional.")
            speak(response_text)

    except Exception as e:
        print(f"Error al conectar con Gemini: {e}")
        speak("Lo siento, no pude procesar tu solicitud en este momento.")

    
# Función principal del asistente
def run_assistant():
    speak("Hola. Soy tu asistente. ¿En qué puedo ayudarte?")
    while True:
        command = listen_command()
        if command:
            if "adiós" in command:
                speak("Hasta luego.")
                break
            else:
                print(f"Comando procesado por la IA: {command}")
                process_command_and_check_json(command)
        else:
            speak("Lo siento, no he podido escuchar nada.")

# Ejecutar el asistente
if __name__ == "__main__":
    run_assistant()