from typing import List
import string
from enum import Enum, auto

SUELO = 0
OBSTACULO = 1
ESTANTERIA = 2
BALIZA = 3

MAX_ROWS = 50
MAX_COLUMNS = 50

class EstadoRobot(Enum):
    PARADO = auto()
    MOVIENDO = auto()
    CALCULANDO = auto()
    ERROR = auto()

class Robot:
    def __init__(self):
        self._position = []
        self._peticio_productes = []
        self._ruta = []
        self._estat = EstadoRobot.PARADO
        self._emoji = "🤖 "

    def get_position(self):
        return self._position[0], self._position[1]
    
    def get_emoji(self) -> string:
        return self._emoji
    
    def set_position(self, x: int, y: int):
        self._position = [x,y]

class Producto:
    def __init__(self, nombre: string, x: int, y: int, emoji):
        self._name = nombre
        self._position = [x, y]
        self._emoji = emoji
    
    def get_position(self):
        return self._position[0], self._position[1]

    def get_name(self) -> string:
        return self._name
    
    def get_emoji(self) -> string:
        return self._emoji

class Estanteria:
    def __init__(self, x: int, y: int):
        self._position = [x, y]
        self._products: List[str] = []

    def get_products(self) -> List[str]:
        return self._products

    def get_position(self):
        return self._position[0], self._position[1]

    def add_product(self, product: str):
        if product not in self._products:
            self._products.append(product)

    def add_products(self, products: List[str]):
        for product in products:
            if product not in self._products:
                self._products.append(product)

    def remove_product(self, product: str):
        if product in self._products:
            self._products.remove(product)



class Mapa:
    def __init__(self, rows: int, columns: int):
        self._rows = rows
        self._columns = columns
        self._map = [
            [SUELO for _ in range(rows)] for _ in range(rows)
        ]
        self._estanterias: List[Estanteria] = []

    def get_valor_coordenada(self, x: int, y: int) -> int:
        if x < 0 or x >= self._rows or y < 0 or y >= self._columns:
            return -1  # Fuera de los límites
        return self._map[y][x]
    
    
    def get_map(self):
        return self._map
    

    def set_obstaculo(self, p1: list, p2: list):
        p1x = p1[0]
        p2x = p2[0]
        p1y = p1[1]
        p2y = p2[1]


        if (
            p1x < 0 or p1x >= self._rows or
            p1y < 0 or p1y >= self._columns or
            p2x < 0 or p2x >= self._rows or
            p2y < 0 or p2y >= self._columns
        ):
            print("Fora de mapa")
            return

        x_min = min(p1y, p2y)
        x_max = max(p1y, p2y)
        y_min = min(p1x, p2x)
        y_max = max(p1x, p2x)

        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                self._map[x][y] = OBSTACULO

    def set_balizas(self):
        self._map[0][0] = BALIZA
        self._map[self._columns-1][0] = BALIZA
        self._map[self._columns-1][self._rows-1] = BALIZA
        self._map[0][self._rows-1] = BALIZA

    
    def set_productos(self, lista_productos: list):

        for producte in lista_productos:
            x, y = producte.get_position()

            if(self.get_valor_coordenada(x, y) == SUELO):
                self._map[y][x] = producte


    def set_robot(self, robot: Robot, x: int, y: int):

        if(self.get_valor_coordenada(x, y) == SUELO):
            robot.set_position(x,y)
            self._map[y][x] = robot



    def imprimir_mapa(self):
        for fila in self._map:
            linea = ""
            for celda in fila:
                if celda == OBSTACULO:
                    linea += "⬛ " 
                if celda == SUELO:
                    linea += "⬜ "
                if celda == BALIZA:
                    linea += "🗼 "
                if type(celda) == Producto:
                    linea += celda.get_emoji()
                if type(celda) == Robot:
                    linea += celda.get_emoji()
            print(linea)


if __name__ == "__main__":

    m = Mapa(13, 13)
    m.set_balizas()
    
    m.set_obstaculo([3,2],[4,10])
    m.set_obstaculo([8,2],[9,10])

    productos = [
        Producto("Tomates", 2, 2, "🍅 "),
        Producto("Leche", 2, 3, "🍶 "),
        Producto("Cafe", 3, 3, "☕️ ") # error
    ]

    m.set_productos(productos)

    compaCompra = Robot()

    m.set_robot(compaCompra, 11, 6)

    m.imprimir_mapa()


