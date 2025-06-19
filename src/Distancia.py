import RPi.GPIO as GPIO
import time

# --- Configuración de los Sensores ---
SENSORES = [
    {'nombre': 'Sensor 1 (Frontal)', 'trig': 18, 'echo': 24}, #Valores de los pines de la Raspberry a los cuales están conectados los Sensores.
    {'nombre': 'Sensor 2 (Izquierda)', 'trig': 20, 'echo': 26},
    {'nombre': 'Sensor 3 (Derecha)', 'trig': 17, 'echo': 27}
]

# --- Configuración de GPIO ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for sensor in SENSORES:
    GPIO.setup(sensor['trig'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)

def medir_distancia(trig_pin, echo_pin):
    GPIO.output(trig_pin, False)
    time.sleep(0.05)

    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    start_time = time.time()
    stop_time = time.time()
    
    timeout_start = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
        if start_time - timeout_start > 0.1:
            return None

    timeout_stop = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()
        if stop_time - timeout_stop > 0.1:
            return None

    tiempo_transcurrido = stop_time - start_time
    distancia = (tiempo_transcurrido * 34300) / 2
    return distancia

def leer_sensores_booleanos():
    """
    Lee los 3 sensores y devuelve una tupla de 3 valores:
    0 si distancia < 15cm, 1 si distancia >= 15cm
    """
    resultados = []
    for sensor in SENSORES:
        dist = medir_distancia(sensor['trig'], sensor['echo'])
        if dist is not None and dist >= 15:
            resultados.append(1)
        else:
            resultados.append(0)
    return tuple(resultados)

# Ejemplo de uso
try:
    print("Iniciando medición. Presiona Ctrl+C para detener.")
    while True:
        estados = leer_sensores_booleanos()
        for i, sensor in enumerate(SENSORES):
            estado = estados[i]
            print(f"{sensor['nombre']}: {'Libre' if estado else 'Obstáculo'}")
        print("-" * 30)
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nMedición detenida por el usuario.")
finally:
    GPIO.cleanup()
    print("Pines GPIO limpiados. Programa finalizado.")
