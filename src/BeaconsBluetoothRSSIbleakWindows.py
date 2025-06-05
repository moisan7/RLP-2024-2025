# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 11:53:28 2025

@author: David
"""

import asyncio
from bleak import BleakScanner
import time
import platform

# Añadido para compatibilidad con entornos interactivos como Spyder o Jupyter
import nest_asyncio
nest_asyncio.apply()

# Lista de direcciones MAC de los beacons objetivo (en minúsculas)
TARGET_MACS = {
    "d8:13:2a:73:6c:7a",
    "a0:a3:b3:2c:8c:be",
    "14:33:5c:30:09:aa",
    "14:33:5c:38:72:ca"
}
TARGET_MACS = set(mac.lower() for mac in TARGET_MACS)

async def scan_beacons():
    print("Escaneando continuamente los beacons especificados...")
    print("Presiona Ctrl + C para detener.\n")

    found_devices = {}

    try:
        while True:
            devices = await BleakScanner.discover(timeout=1.0)

            for dev in devices:
                mac = dev.address.lower()
                if mac in TARGET_MACS:
                    rssi = dev.rssi
                    found_devices[mac] = rssi
                    print(f"[{time.strftime('%H:%M:%S')}] {mac} - RSSI: {rssi} dB")
    except KeyboardInterrupt:
        print("\n\nEscaneo detenido por el usuario.")
        print("Últimos valores RSSI detectados:")
        for mac, rssi in found_devices.items():
            print(f"{mac} - RSSI: {rssi} dB")
        return found_devices

# Solo para Windows: usa el selector de bucle compatible
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Ejecuta el bucle sin romper el entorno de Spyder
loop = asyncio.get_event_loop()
loop.create_task(scan_beacons())

# Mantener el bucle activo indefinidamente
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
