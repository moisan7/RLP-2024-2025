import json
import requests
from utils.ruta import ruta_optima_super
from utils.mapa import construir_mapa, obtener_posicion_caja

def calcular_ruta_http(request):
    datos = request.get_json()
    inicio = tuple(datos["inicio"])
    objetivos = [tuple(obj) for obj in datos["objetivos"]]
    lista_de_la_compra = datos["lista_de_la_compra"]
    url_consultar_mapa = "https://europe-west1-compacompraapp.cloudfunctions.net/consultarMapaBD"
    datos_mapa = requests.get(url_consultar_mapa)
    mapa = construir_mapa(datos_mapa.json())
    url_consultar_caja_registradora = "https://europe-west1-compacompraapp.cloudfunctions.net/consultarCajaRegistradoraBD"
    datos_caja = requests.get(url_consultar_caja_registradora)
    caja_ubi = obtener_posicion_caja(datos_caja.json())
    fin = caja_ubi
    cuadricula = mapa
    resultado = ruta_optima_super(inicio, objetivos, lista_de_la_compra, fin, cuadricula)
    def serializar(o):
        if isinstance(o, str):
            return o
        if isinstance(o, (list, tuple)):
            return [serializar(x) for x in o]
        return o
    resultado_serializado = {k: serializar(v) for k, v in resultado.items()}
    return json.dumps(resultado_serializado), 200, {"Content-Type": "application/json"}
