from tenacity import retry, wait_fixed, stop_after_attempt
import random

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def get_game_statistics(game_id):
    """
    Intenta recuperar el promedio de calificaciones y el número total de reseñas de un videojuego específico.
    """
    try:
        # Simulamos una posible falla en la consulta a la base de datos
        if random.choice([True, False]):  # Random para simular fallo en la conexión
            raise ConnectionError("Error en la conexión a la base de datos.")

        # Datos simulados que regresaría la base de datos en caso de éxito
        return {
            "average_rating": 4.3,
            "total_reviews": 150
        }

    except ConnectionError as e:
        print(f"Fallo de conexión: {e}")
        raise  # Relevante para que tenacity vuelva a intentar la conexión

# Llamada al método de ejemplo para el videojuego con id "game_001"
game_id = "game_001"
try:
    stats = get_game_statistics(game_id)
    print(f"Promedio de calificación: {stats['average_rating']}")
    print(f"Total de reseñas: {stats['total_reviews']}")
except Exception as e:
    print("No se pudo recuperar la información del videojuego después de varios intentos.")
