# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import subprocess
import time 
import numpy as np
import math

# mac_address1 = "9C:73:B1:4F:75:94"  # Adreça MAC del dispositiu Bluetooth vinculat. S23Ultra
# MACs dels Mobils fent de Beacons Bluetooth.
macs = {
    "b2": "DC:F7:56:13:74:9D",  # (0,2)
    "b1": "88:9F:6F:5F:B5:0B",  # (2,2)
    "b3": "90:06:28:17:C5:A4"   # (0, -2)
    # Es poden afegir mes si fa falta.
}

#Posicions ficticies i FIXES dels 4 Beacons Simulats amb Mobils.
#Es pot jugar amb els valors per anar cal·librant el sistema.
beacons = {
    "b1": (-2, 2),
    "b2": (5, 2),
    "b3": (-2, -2),
    "b4": (2, 0)
}

def potenciaRSSI(mac):
    try:
        output = subprocess.check_output(["hcitool", "rssi", mac], stderr=subprocess.STDOUT)
        output = output.decode()
        rssi_value = int(output.strip().split()[-1])
        return rssi_value
    except subprocess.CalledProcessError as e:
        return None
    
def rssiDistancia(rssi, tx_power, n=2):
    #El valor de n en interiors ha d'anar entre 2 i 4. Es tracta d'un factor d'atenuacio.
    distancia = 10 * ((tx_power - rssi) / (10 * n))
    return distancia

# Trilateració fent servir Minims Quadrats.
def trilateracioMultiples(beacon_positions, distances):
    A = []
    b = []
    for i in range(1, len(beacon_positions)):
        x0, y0 = beacon_positions[0]
        xi, yi = beacon_positions[i]
        di2 = distances[i] ** 2
        d02 = distances[0] ** 2
        A.append([2*(xi - x0), 2*(yi - y0)])
        b.append([d02 - di2 + xi**2 + yi**2 - x0**2 - y0**2])
    A = np.array(A)
    b = np.array(b)
    pos, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return pos.flatten()

senyal = [] #Per fer la prova de guardar la intensitat de la senyal Bluetooth.
senyal2 = []
# Seguimiento en tiempo real
print("Vol començar a registrar la intensitat del senyal bluetooth? En cas afirmatiu premi la tecla s.")
entrada = input()
comptador = 0

while entrada == 's':
    rssi_values = {}
    distances = []
    positions = []

    # Leer RSSI y calcular distancia
    for key, mac in macs.items():
        rssi = potenciaRSSI(mac)
        if rssi is not None:
            dist = rssiDistancia(rssi,0, 2)
            print(f"{key} | RSSI: {rssi} dBm | Distancia estimada: {dist:.2f} m")
            distances.append(dist)
            positions.append(beacons[key])
        else:
            print(f"{key} | Error al leer RSSI")

    # Calcular posición si hay al menos 3 distancias
    if len(distances) >= 3:
        pos = trilateracioMultiples(positions, distances)
        print(f"📍 Posició estimada del receptor: x={pos[0]:.2f}, y={pos[1]:.2f}")
    else:
        print("No hi ha prou Becaons Bluetooth connectats per calcular la distanciaposicio Real.")

    time.sleep(1)
    comptador += 1
    if comptador % 100 == 0:
        print("Vol seguir registrant? Premi la tecla s.")
        entrada = input()