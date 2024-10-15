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
        gameId = "Final Fantasy XV"
        userId = "UsuarioSentimiento002"
        rating = 8
        review = "Gameplay perfecto, pero me hubiera gustado más contenido adicional."
        category = "RPG"

        gameId1 = "Assassin's Creed: Syndicate"
        rating1 = 6
        review1 = "Gameplay bueno, pero no resalta en su variedad de niveles ni objetivos."
        category1 = "Aventura"
        
        gameId2 = "God of War"
        rating2 = 9
        review2 = "Gameplay espectacular, buena narrativa, únicamente mejoraría la duración."
        category2 = "RPG"

        gameId3 = "Gotham Knights"
        rating3 = 4
        review3 = "Buenos personajes poco desarrollados, estética correcta, pero con una variedad de niveles malísima."
        category3 = "Acción"


        # Enviar el mensaje
        send_message(client, gameId, userId, rating, review, category)
        send_message(client, gameId1, userId, rating1, review1, category1)
        send_message(client, gameId2, userId, rating2, review2, category2)
        send_message(client, gameId3, userId, rating3, review3, category3)
        
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