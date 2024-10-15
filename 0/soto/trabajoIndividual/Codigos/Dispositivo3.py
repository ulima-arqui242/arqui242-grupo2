from azure.iot.device import IoTHubDeviceClient
import time

# Cadena de conexión del dispositivo (obtenida del IoT Hub)
CONNECTION_STRING = "HostName=ResenasJuegosSentimientosHub.azure-devices.net;DeviceId=UsuarioSentimiento003;SharedAccessKey=v/lWWYg7Qj5NjcXus9jnAutYyh6398f4XbbbADz5ufA="
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
        gameId = "Super Mario Wonder"
        userId = "UsuarioSentimiento003"
        rating = 10
        review = "Soy fan de Mario y esto es todo lo que imaginas de un juego de Mario, sé que la banda sonora no es novedosa, pero retoma temas espectaculares de antaño"
        category = "Plataformas"

        gameId1 = "Assassin's Creed: Syndicate"
        rating1 = 3
        review1 = "Más de lo mismo en la saga Assassin's Creed, espero Ubisoft cambie algo, porque siento que cada juego que sale es igual que el anterior."
        category1 = "Aventura"
        
        gameId2 = "The Legend of Zelda: Breath of the Wild"
        rating2 = 8
        review2 = "Me encanta el juego, las mecánicas, la banda sonora, el reto que representa completarlo, pero no me gustó que algunas misiones secundarias se sienten algo repetitivas."
        category2 = "RPG"

        gameId3 = "Gotham Knights"
        rating3 = 8
        review3 = "Me gustan los juegos donde se tienen que vencer hordas de enemigos y amo batman y la batifamilia."
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
