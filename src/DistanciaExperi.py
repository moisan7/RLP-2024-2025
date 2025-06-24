import RPi.GPIO as GPIO
import time
import serial

# --- Serial con ESP32 ---
esp = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)  # Espera a que ESP32 reinicie

# --- Configuración de los Sensores ---
SENSORES = [
    {'nombre': 'Frontal', 'trig': 18, 'echo': 24},
    {'nombre': 'Izquierda', 'trig': 20, 'echo': 26},
    {'nombre': 'Derecha', 'trig': 17, 'echo': 27}
]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for sensor in SENSORES:
    GPIO.setup(sensor['trig'], GPIO.OUT)
    GPIO.setup(sensor['echo'], GPIO.IN)

def medir_distancia(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.05)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    timeout = time.time()
    while GPIO.input(echo) == 0:
        if time.time() - timeout > 0.1:
            return None
        start = time.time()

    timeout = time.time()
    while GPIO.input(echo) == 1:
        if time.time() - timeout > 0.1:
            return None
        stop = time.time()

    elapsed = stop - start
    return (elapsed * 34300) / 2

def leer_sensores_booleanos():
    estados = []
    for sensor in SENSORES:
        dist = medir_distancia(sensor['trig'], sensor['echo'])
        if dist is not None and dist >= 15:
            estados.append(1)
        else:
            estados.append(0)
    return tuple(estados)

# --- Control principal ---
try:
    print("Iniciando vigilancia de sensores...")
    en_pausa = False

    while True:
        estados = leer_sensores_booleanos()
        libre = all(e == 1 for e in estados)

        if not libre and not en_pausa:
            print("Obstáculo detectado — Pausando robot.")
            esp.write(b'P')
            en_pausa = True

        elif libre and en_pausa:
            print("Ruta despejada — Reanudando robot.")
            esp.write(b'C')
            en_pausa = False

        # Mostrar estado
        for i, sensor in enumerate(SENSORES):
            print(f"{sensor['nombre']}: {'Libre' if estados[i] else 'Obstáculo'}")
        print("-" * 30)
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    GPIO.cleanup()
    esp.close()
