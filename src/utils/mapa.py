import numpy as np

def construir_mapa(mapa_json):
    ancho = mapa_json['ancho']
    largo = mapa_json['largo']
    obstaculos = mapa_json['obstaculos']
    cuadricula = np.zeros((largo, ancho), dtype=int)
    for obs in obstaculos:
        x, y = obs['x'], obs['y']
        cuadricula[y, x] = 1
    return cuadricula

def obtener_posicion_caja(caja_json):
    if not caja_json["cajas_registradoras"]:
        raise ValueError("No hay cajas registradoras en el mapa.")
    caja = caja_json["cajas_registradoras"][0]
    return (caja["x"], caja["y"])
