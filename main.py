from flask import Flask, request
import subprocess

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Diccionario que mapea nombres de programas a sus rutas completas.
# Esto hace que el script sea más flexible y fácil de configurar.
PROGRAM_PATHS = {
    'vscode': "C:\\Users\\paulh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    # Agrega otros programas aquí si lo deseas.
    # Por ejemplo: 'chrome': "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    # 'notepad': "notepad.exe"
}

# Esta ruta manejará las peticiones POST enviadas a /ejecutar-comando
@app.route('/ejecutar-comando', methods=['POST'])
def ejecutar_comando():
    """
    Procesa los comandos JSON recibidos y ejecuta la acción correspondiente.
    """
    try:
        # Intenta obtener los datos JSON de la petición
        data = request.json
        
        # Verifica si los datos y la acción esperada están presentes
        if 'accion' in data and data['accion'] == 'abrir_programa':
            nombre_programa_json = data.get('nombre_programa')

            if nombre_programa_json:
                # Busca la ruta completa en nuestro diccionario
                ruta_ejecutable = PROGRAM_PATHS.get(nombre_programa_json)

                if ruta_ejecutable:
                    try:
                        # subprocess.Popen() ejecuta el programa sin esperar a que se cierre
                        subprocess.Popen([ruta_ejecutable])
                        
                        respuesta = f"Se ha solicitado abrir el programa {nombre_programa_json}."
                        print(f"Éxito: {respuesta}")
                        return {"mensaje": respuesta, "status": "recibido"}
                    
                    except FileNotFoundError:
                        mensaje_error = f"Error: No se encontró el programa en la ruta especificada: {ruta_ejecutable}"
                        print(mensaje_error)
                        return {"mensaje": mensaje_error, "status": "error"}
                else:
                    mensaje_error = f"Error: El programa '{nombre_programa_json}' no está en la lista de programas configurados."
                    print(mensaje_error)
                    return {"mensaje": mensaje_error, "status": "error"}
            else:
                mensaje_error = "Error: El campo 'nombre_programa' está vacío en el JSON."
                print(mensaje_error)
                return {"mensaje": mensaje_error, "status": "error"}

        # Si la acción en el JSON no es la esperada, devuelve un error
        mensaje_error = "Error: Comando no reconocido. Asegúrate de que el campo 'accion' sea 'abrir_programa'."
        print(mensaje_error)
        return {"mensaje": mensaje_error, "status": "error"}

    except Exception as e:
        # Maneja cualquier otro error inesperado
        error_inesperado = f"Error interno del servidor: {e}"
        print(error_inesperado)
        return {"mensaje": error_inesperado, "status": "error"}, 500

# Inicia el servidor Flask en el puerto 5000
if __name__ == '__main__':
    # La opción 'debug=True' reinicia el servidor automáticamente con los cambios
    # Se recomienda usar solo para el desarrollo
    app.run(port=5000, debug=True)