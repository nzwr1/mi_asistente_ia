# Importa las librerías necesarias
import requests
import json

# URL del servidor local de tu agente
url = 'http://127.0.0.1:5000/ejecutar-comando'

# Define el comando JSON que quieres enviar
# El valor de "nombre_programa" debe coincidir con una clave en el diccionario de tu agente
comando = {
    "accion": "abrir_programa",
    "nombre_programa": "vscode" 
}

# Define el encabezado de la petición
headers = {'Content-Type': 'application/json'}

try:
    # Envía la petición POST al agente local
    response = requests.post(url, data=json.dumps(comando), headers=headers)
    response.raise_for_status()  # Lanza un error para códigos de estado 4xx/5xx

    # Imprime la respuesta del servidor
    print("Respuesta del servidor:")
    print(response.json())

except requests.exceptions.RequestException as e:
    # Maneja cualquier error en la petición
    print(f"Error al enviar la petición: {e}")