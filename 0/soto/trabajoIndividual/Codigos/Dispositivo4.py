from azure.iot.device import IoTHubDeviceClient
import time

# Cadena de conexión del dispositivo (obtenida del IoT Hub)
CONNECTION_STRING = "HostName=ResenasJuegosSentimientosHub.azure-devices.net;DeviceId=UsuarioSentimiento004;SharedAccessKey=BUPuXRVk3bGe9ynqhyFbcy2sYtx1+/v9DQiRXpn5D6c="
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
        userId = "UsuarioSentimiento004"
        rating = 9
        review = "Me encantó como juego de Mario, es divertidísimo y candidato perfecto al GOTY; sin embargo, la banda sonora pudo proponer algo más original."
        category = "Plataformas"

        gameId1 = "Elden Ring"
        rating1 = 10
        review1 = "Todo es perfecto en este juego, admito que no es para todos, pero si eres amante de los Souls, este juego es el punto máximo al que pudieron llegar."
        category1 = "Aventura"
        
        gameId2 = "The Legend of Zelda: Breath of the Wild"
        rating2 = 10
        review2 = "El mejor juego de mundo abierto que Nintendo haya realizado, me encanta todo de este juego, lo recomiendo y es una opción imperdible en Nintendo Switch."
        category2 = "RPG"

        gameId3 = "Gotham Knights"
        rating3 = 1
        review3 = "No me gustó nada de este juego, sobre todo por la expectativa que tenía y el potencial que parecía tener, muy repetitivo y una historia tan floja que derrumba todo lo construido por juegos del mundo de batman."
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
