from azure.iot.device import IoTHubDeviceClient
import time

# Cadena de conexión del dispositivo (obtenida del IoT Hub)
CONNECTION_STRING = "HostName=ResenasJuegosSentimientosHub.azure-devices.net;DeviceId=UsuarioSentimiento002;SharedAccessKey=HPod5z043EBlix71JTfGUi8QK2H9K6VlreKFFGGjR60="

# Crear cliente de dispositivo IoT
def create_client():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

# Enviar mensaje (reseña o calificación)
def send_message(client, gameId, userId, rating, review, category):
    message = f'{{"gameId": "{gameId}", "userId": "{userId}", "rating": {rating}, "review": "{review}", "category": "{category}"}}'
    print(f"Enviando mensaje: {message}")
    client.send_message(message)
    print("Mensaje enviado exitosamente.")

def main():
    print("Conectando al IoT Hub...")
    client = create_client()
    client.connect()

    try:
        # Ejemplo de reseña y calificación
        gameId = "Minecraft"
        userId = "UsuarioSentimiento002"
        rating = 7
        review = "Un clásico del gaming, un juego sencillo con gráficos en pixelart y que presenta un mundo abierto bastante extenso y con muchas posibilidades, la historia es prácticamente inexistente."
        category = "sandbox"


        # Enviar el mensaje
        send_message(client, gameId, userId, rating, review, category)
        
        # Esperar un momento antes de cerrar la conexión
        time.sleep(5)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Desconectar el cliente
        client.disconnect()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
