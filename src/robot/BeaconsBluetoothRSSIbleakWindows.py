#!/usr/bin/env python3
# -- coding: utf-8 --

"""
Created on Thu May 29 11:44:31 2025
@author: servito
"""

import asyncio
from bleak import BleakScanner
import time
import platform

# Lista de direcciones MAC de los beacons objetivo (en minúsculas)
TARGET_MACS = {
    "d8:13:2a:73:6c:7a",
    "a0:a3:b3:2c:8c:be",
    "14:33:5c:30:09:aa",
    "14:33:5c:38:72:ca"
}


### cambiar segun posicionamiento beacons
idmac = {}
idmac["d8:13:2a:73:6c:7a"] = "bottom-left"
idmac["a0:a3:b3:2c:8c:be"] = "bottom-right"
idmac["14:33:5c:30:09:aa"] = "top-right"
idmac["14:33:5c:38:72:ca"] = "top-left"

# Normaliza a minúsculas
TARGET_MACS = set(mac.lower() for mac in TARGET_MACS)

# Valor de alpha para el filtro exponencial (más cercano a 1 = más sensible)
ALPHA = 0.2


def estimate_distance(rssi, tx_power=-70, n=2.2):
    """
    Estima la distancia al beacon en metros a partir del RSSI.
    tx_power: RSSI a 1 metro del beacon (debes ajustarlo según tu hardware real)
    n: factor ambiental (2=espacio libre, >2=con obstáculos)
    """
    if rssi == 0:
        return None  # RSSI 0 significa señal inválida
    ratio_db = (tx_power - rssi) / (10 * n)
    return round(10 ** ratio_db, 2)


async def scan_beacons():
    print("Escaneando continuamente los beacons especificados...")
    print("Presiona Ctrl + C para detener.\n")

    raw_rssi = {}
    filtered_rssi = {}

    try:
        while True:
            devices = await BleakScanner.discover(timeout=1.0)

            for dev in devices:
                mac = dev.address.lower()
                if mac in TARGET_MACS:
                    rssi = dev.rssi

                    # Filtro de media móvil exponencial (EMA)
                    if mac in filtered_rssi:
                        filtered_rssi[mac] = ALPHA * rssi + (1 - ALPHA) * filtered_rssi[mac]
                    else:
                        filtered_rssi[mac] = rssi  # Primer valor sin filtrar

                    raw_rssi[mac] = rssi

                    #print(f"[{time.strftime('%H:%M:%S')}] {mac} - RSSI: {rssi} dB | Filtrado: {filtered_rssi[mac]:.2f} dB")
                    
            for mac in TARGET_MACS:
                if mac in raw_rssi:
                    distance = estimate_distance(raw_rssi[mac])
                    print(f"[{time.strftime('%H:%M:%S')}] {idmac[mac]} - RSSI: {raw_rssi[mac]} dB - Distancia estimada: {distance} m ")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] {idmac[mac]} - No detectado")
            print("--------------------------------------------------------------")


    except KeyboardInterrupt:
        print("\n\nEscaneo detenido por el usuario.")
        print("Últimos valores RSSI detectados:")
        for mac in filtered_rssi:  
            print(f"{mac} - RSSI filtrado: {filtered_rssi[mac]:.2f} dB")
        return filtered_rssi


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(scan_beacons())
