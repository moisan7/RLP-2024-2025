#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 24 19:22:59 2025

@author: servito
"""

import asyncio
from bleak import BleakScanner
import time

async def scan_beacons_until_interrupt(target_macs):
    """
    Escanea dispositivos Bluetooth LE filtrando por direcciones MAC específicas.

    Parámetros:
        target_macs (iterable): Lista o conjunto de direcciones MAC (en cualquier formato).

    Devuelve:
        dict: Diccionario con MACs detectadas como claves y sus RSSI como valores.
    """
    target_macs = set(mac.lower() for mac in target_macs)
    found_devices = {}

    print("Escaneando continuamente los beacons especificados...")
    print("Presiona Ctrl + C para detener.\n")

    def detection_callback(device, advertisement_data):
        mac = device.address.lower()
        if mac in target_macs:
            found_devices[mac] = device.rssi
            print(f"[{time.strftime('%H:%M:%S')}] {mac} - RSSI: {device.rssi} dB")

    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)

    try:
        while True:
            await scanner.start()
            await asyncio.sleep(1.0)
            await scanner.stop()
    except KeyboardInterrupt:
        print("\n\nEscaneo detenido por el usuario.")
        print("Últimos valores RSSI detectados:")
        for mac, rssi in found_devices.items():
            print(f"{mac} - RSSI: {rssi} dB")

    return found_devices


if __name__ == "__main__":
    TARGET_MACS = {
        "d8:13:2a:73:6c:7a",
        "a0:a3:b3:2c:8c:be",
        "14:33:5c:30:09:aa",
        "14:33:5c:38:72:ca"
    }
    asyncio.run(scan_beacons_until_interrupt(TARGET_MACS))