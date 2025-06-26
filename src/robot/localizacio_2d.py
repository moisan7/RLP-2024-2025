from math import sqrt

class Objeto:
    def __init__(self, nombre, tipo, emoji, coord):
        self.nombre = nombre
        self.tipo = tipo
        self.emoji = emoji
        self.coord = coord

a = Objeto("Baliza_A", "baliza", "🗼", (0, 0))
b = Objeto("Baliza_B", "baliza", "🗼", (0, 9))
c = Objeto("Baliza_C", "baliza", "🗼", (9, 0))
d = Objeto("Baliza_D", "baliza", "🗼", (9, 9))
r = Objeto("CompaCompra", "robot", "🤖", (2, 2))
p = Objeto("Llet", "producte", "📦", (5, 7))
u = Objeto("Client", "usuari", "🧍", (3, 2))

mapa_supermercat = [
    [a, 1, 1, 1, 1, 1, 1, 1, 1, b],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, r, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [c, 1, 1, 1, 1, 1, 1, 1, 1, d],
]

# Funció per imprimir el mapa amb símbols visuals
def imprimir_mapa(mapa):
    for fila in mapa:
        linea = ""
        for celda in fila:
            if celda == 1:
                linea += "⬛ "  # obstacle
            if celda == 0:
                linea += "⬜ "  # espai lliure
            if isinstance(celda, Objeto):
                linea += f"{celda.emoji} " 
        print(linea)

def distancia_euclidiana(A, B):
    # d(A, B) = √(Ax - Bx)^2 + (Ay - By)^2
    if type(A) != tuple or type(B) != tuple:
        TypeError("Argumento A o B no valido!")
    return round(sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2), 2)

def trilateracion(p1, p2, p3, r1, r2, r3):
    # CIRCULO
    # (x - xi)^2 + (y - yi)^2 = di^2

    # COORDENADAS
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2

    D = 2 * (x3 - x1)
    E = 2 * (y3 - y1)
    F = r1**2 - r3**2 - x1**2 + x3**2 - y1**2 + y3**2

     # Resolució de sistema lineal: A*x + B*y = C ; D*x + E*y = F
    denom = A*E - B*D
    if denom == 0:
        raise ValueError("Les balises estan en línia o les distàncies no són consistents.")

    x = (C*E - B*F) / denom
    y = (A*F - C*D) / denom
    x = round(x)
    y = round(y)
    return (x, y)

# Executar la funció
imprimir_mapa(mapa_supermercat)

r1 = distancia_euclidiana(a.coord, r.coord)
r2 = distancia_euclidiana(b.coord, r.coord)
r3 = distancia_euclidiana(c.coord, r.coord)
print(f"Trilateracion ABC a R. Coordenadas {trilateracion(a.coord, b.coord, c.coord, r1, r2, r3)}")
