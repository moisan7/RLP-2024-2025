import numpy as np
import heapq
import math
from itertools import permutations

def calcular_ruta(inicio, objetivo, cuadricula):
    def heuristica(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    def vecinos(nodo):
        x, y = nodo
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(cuadricula[0]) and 0 <= ny < len(cuadricula):
                if cuadricula[ny][nx] == 0:
                    yield (nx, ny)
    open_set = []
    heapq.heappush(open_set, (heuristica(inicio, objetivo), 0, inicio))
    came_from = {}
    g = {inicio: 0}
    while open_set:
        _, coste, actual = heapq.heappop(open_set)
        if actual == objetivo:
            ruta = [actual]
            while actual in came_from:
                actual = came_from[actual]
                ruta.append(actual)
            return ruta[::-1]
        for vecino in vecinos(actual):
            tentative_g = g[actual] + 1
            if vecino not in g or tentative_g < g[vecino]:
                came_from[vecino] = actual
                g[vecino] = tentative_g
                f = tentative_g + heuristica(vecino, objetivo)
                heapq.heappush(open_set, (f, tentative_g, vecino))
    return None

def matriz_distancias(nodos, cuadricula):
    n = len(nodos)
    dist = [[0]*n for _ in range(n)]
    rutas = {}
    for i in range(n):
        for j in range(i+1, n):
            ruta = calcular_ruta(nodos[i], nodos[j], cuadricula)
            if ruta is None:
                return None, None
            distancia = len(ruta)-1
            dist[i][j] = dist[j][i] = distancia
            rutas[(i, j)] = rutas[(j, i)] = ruta
    return dist, rutas

def tsp_inicio_objetivos_fin(dist, inicio_idx, objetivos_idx, fin_idx):
    mejor_orden = None
    mejor_coste = float('inf')
    for perm in permutations(objetivos_idx):
        indices = [inicio_idx] + list(perm) + [fin_idx]
        coste = sum(dist[indices[i]][indices[i+1]] for i in range(len(indices)-1))
        if coste < mejor_coste:
            mejor_coste = coste
            mejor_orden = indices
    return mejor_orden, mejor_coste

def ruta_optima_super(inicio, objetivos, lista_de_la_compra, fin, cuadricula):
    nodos = [inicio] + objetivos + [fin]
    inicio_idx = 0
    fin_idx = len(nodos) - 1
    objetivos_idx = list(range(1, len(nodos)-1))
    dist, rutas = matriz_distancias(nodos, cuadricula)
    if dist is None:
        raise ValueError("Hay objetivos sin ruta posible.")
    mejor_orden, mejor_coste = tsp_inicio_objetivos_fin(dist, inicio_idx, objetivos_idx, fin_idx)
    rutas_por_tramo = []
    orden_objetivos = []
    compra_ordenada = []
    for idx in range(1, len(mejor_orden)-1):
        orden_objetivos.append(nodos[mejor_orden[idx]])
        compra_ordenada.append(lista_de_la_compra[mejor_orden[idx]-1])
    for i in range(len(mejor_orden)-1):
        a, b = mejor_orden[i], mejor_orden[i+1]
        tramo = rutas[(a, b)]
        rutas_por_tramo.append(tramo)
    return {
        "ruta_optima": rutas_por_tramo,
        "orden_objetivos": orden_objetivos,
        "compra_ordenada": compra_ordenada,
    }
