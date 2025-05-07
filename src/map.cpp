using namespace std;
#include <iostream>
#include <vector>
#include <string>

struct Coordenada {
	int x;
	int y;
};

#define SUELO 0
#define OBSTACULO 1
#define ESTANTERIA 2

#define MAX_ROWS 50
#define MAX_COLUMNS 50

class Estanteria {

public:

	Estanteria(int x, int y) : m_position({ x, y }) {}

	vector<string> getProducts() const { return m_products; }
	Coordenada getPosition() const { return m_position; }

	void addProduct(const string& product) {

		// Comprueba si el producto ya existe, si existe no lo añade
		for (auto it = m_products.begin(); it != m_products.end(); ++it) {
			if (*it == product) {
				return;
			}
		}

		// Si no existe lo añade
		m_products.push_back(product);
	}

	void addProduct(vector<string> products) {

		// Comprueba si los producto ya existen, los que existan no se añaden
		for (auto it = products.begin(); it != products.end(); ++it) {
			for (auto it2 = m_products.begin(); it2 != m_products.end(); ++it2) {
				if (*it == *it2) {
					products.erase(it);
				}
			}
		}

		// Si no existen los añade
		for (auto it = products.begin(); it != products.end(); ++it) {
			m_products.push_back(*it);
		}
	}

	void removeProduct(const string& product) {

		for (auto it = m_products.begin(); it != m_products.end(); ++it) {
			if (*it == product) {
				m_products.erase(it);
				break;
			}
		}
	}

private:
	Coordenada m_position;
	vector<string> m_products;
};




class Mapa {
	
public:
	Mapa(int rows, int columns) : m_rows(rows), m_columns(columns), m_map(rows, vector<int>(columns, SUELO))
	{}

	int getValorCoordenada(int x, int y) const {
		if (x < 0 || x >= m_rows || y < 0 || y >= m_columns) {
			return -1; // Fuera de los límites
		}
		return m_map[x][y];
	}

private:
	int m_rows;
	int m_columns;
	vector<Estanteria> m_estanterias;
	vector<vector<int>> m_map;
};


int main()
{
	// pruebas
	Mapa m = Mapa(3, 3); // Crea un mapa de 3x3
	cout << m.getValorCoordenada(0,0) << endl;
	return 0;
}
