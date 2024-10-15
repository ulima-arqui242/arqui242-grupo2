from azure.iot.device import IoTHubDeviceClient
import time

# Cadena de conexión del dispositivo (obtenida del IoT Hub)
CONNECTION_STRING = "HostName=ResenasJuegosSentimientosHub.azure-devices.net;DeviceId=UsuarioSentimiento001;SharedAccessKey=XIyqvTF+V47tcwCDqDkXt/gHKZ5Awoly5oRM3MumW94="

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
        userId = "UsuarioSentimiento001"
        rating = 6
        review = "Amo el gameplay, pero los gráficos son del pasado."
        category = "RPG"

        gameId1 = "Super Mario Wonder"
        rating1 = 8
        review1 = "Mecánicas divertidas, escenarios llenos de color, pero una historia que pudo estar mejor."
        category1 = "Plataformas"
        
        gameId2 = "The Legend of Zelda: Breath of the Wild"
        rating2 = 10
        review2 = "Perfecto, buenas mecáncias, retador y con un ingenio para los niveles y batallas con jefes."
        category2 = "RPG"

        gameId3 = "Assassin's Creed: Syndicate"
        rating3 = 7
        review3 = "Me encanta la saga y este juego cumple con entregar una buena historia, pero las misiones secundarias son aburridísimas."
        category3 = "Aventura"

        gameId4 = "God of War"
        rating4 = 5
        review4 = "Es un buen juego, pero siento que pierde la esencia que tenían los antiguos God Of War en los que lo más importante es eliminar enemigos, este es más un RPG."
        category4 = "RPG"

        # Enviar el mensaje
        send_message(client, gameId, userId, rating, review, category)
        send_message(client, gameId1, userId, rating1, review1, category1)
        send_message(client, gameId2, userId, rating2, review2, category2)
        send_message(client, gameId3, userId, rating3, review3, category3)
        send_message(client, gameId4, userId, rating4, review4, category4)
        
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
