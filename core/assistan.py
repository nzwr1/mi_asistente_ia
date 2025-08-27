import sys
import os
import speech_recognition as sr
import pyttsx3 
import google.generativeai as genai
from dotenv import load_dotenv


# Cargar las variables del archivo .env
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configura la API con tu clave
genai.configure(api_key=GEMINI_API_KEY)

# Inicializa el modelo de Gemini
model = genai.GenerativeModel('models/gemini-2.5-pro')

# Función para procesar un comando con la IA
def process_command_gemini(command):
    try:
        # Envía tu comando al modelo
        response = model.generate_content(command)
        return response.text
    except Exception as e:
        print(f"Error al conectar con Gemini: {e}")
        return "Lo siento, no pude procesar tu solicitud en este momento."

# Inicializamos el reconocimiento de voz y texto
listener = sr.Recognizer()
engine =  pyttsx3.init()

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
    
# Función para procesar la lógica del comando con la IA
def process_command(command):
    try:
        response = model.generate_content(command)
        return response.text
    except Exception as e:
        print(f"Error al conectar con Gemini: {e}")
        return "Lo siento, no pude procesar tu solicitud en este momento."
    
# Función principal del asistente
def run_assistant():
    speak("Hola. Soy tu asistente. ¿En qué puedo ayudarte?")
    while True:
        command = listen_command()
        if command:
            if "adiós" in command:
                speak("Hasta luego.")
                break
            elif "adiós" in command:
                speak("Hasta luego.")
                break
            else:
                print(f"Comando procesado por la IA: {command}")
                reply = process_command(command)
                print(f"Respuesta de la IA: {reply}")
                speak(reply)
        else:
            speak("Lo siento, no he podido escuchar nada.")

# Ejecutar el asistente
if __name__ == "__main__":
    run_assistant()