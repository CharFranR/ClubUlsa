import serial
import time
import requests
from datetime import datetime

SERIAL_PORT = 'COM11'
BAUD_RATE = 115200
API_URL = 'http://localhost:5001/insertar'
CONFIG_URL = 'http://localhost:5001/config'

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Conectado a {SERIAL_PORT} a {BAUD_RATE} baudios.")
except Exception as e:
    print(f"No se pudo abrir el puerto serial: {e}")
    exit(1)

def enviar_datos(data):
    while True:
        try:
            response = requests.post(API_URL, json=data, timeout=3)
            print(f"Respuesta del servidor: {response.json()}")
            return
        except Exception:
            print("Servidor no disponible, reintentando en 2 segundos...")
            time.sleep(2)

print("Esperando datos del ESP32...")

ultimo_envio_config = 0

while True:
    try:
        # 1. Recibir datos desde el ESP32
        line = ser.readline().decode('utf-8').strip()
        if line:
            parts = line.split(',')
            if len(parts) == 6:
                data = {
                    'temperatura': float(parts[0]),
                    'caudal': float(parts[1]),
                    'nivel': float(parts[2]),
                    'posicion': int(parts[3]),
                    'paro': parts[4].lower() in ('true', '1'),
                    'finalizado': parts[5].lower() in ('true', '1'),
                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                print(f"[{data['fecha']}] Temp: {data['temperatura']}, Caudal: {data['caudal']}, Nivel: {data['nivel']}")
                enviar_datos(data)

        # 2. Cada 5 segundos pedir config y enviarla al ESP32
        if time.time() - ultimo_envio_config > 5:
            try:
                config = requests.get(CONFIG_URL).json()
                setTemp = config['setTemp']
                setNivel = config['setNivel']
                ser.write(f"{setTemp},{setNivel}\n".encode('utf-8'))
                print(f"Enviado setpoints a ESP32: {setTemp},{setNivel}")
            except Exception as e:
                print(f"No se pudo obtener config: {e}")
            ultimo_envio_config = time.time()

    except Exception as e:
        print(f"Error procesando línea: {e}")
