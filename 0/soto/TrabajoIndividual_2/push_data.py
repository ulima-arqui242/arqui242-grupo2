import random
import time
from datetime import datetime
import mysql.connector

# Configuración de conexión
config = {
    'user': 'root',  # Usuario por defecto en StarRocks
    'password': '',  # Si tienes contraseña, añádela aquí
    'host': '127.0.0.1',
    'port': 9030,    # Puerto por defecto
    'database': 'realtime_demo'
}

# Generador de datos
def generate_data():
    return {
        'id': random.randint(1, 100),
        'timestamp': datetime.now(),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 70.0), 2)
    }

# Inserta datos en StarRocks
def push_data(cursor, data):
    query = """
    INSERT INTO sensor_data (id, timestamp, temperature, humidity)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (data['id'], data['timestamp'], data['temperature'], data['humidity']))

def main():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    try:
        while True:
            data = generate_data()
            push_data(cursor, data)
            connection.commit()
            print(f"Data pushed: {data}")
            time.sleep(2)  # Cambia el intervalo si es necesario
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
