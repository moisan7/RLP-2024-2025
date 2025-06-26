import '../models/aliment.dart';
import 'package:flutter/material.dart';

int anchoMapa = 5;
int largoMapa = 5;
int robotX = 0;
int robotY = 0;
Set<Point> obstacles = {};
final List<Point> ruta = [];

Widget buildMapaWidget(
  BuildContext context, {
  required int anchoMapa,
  required int largoMapa,
  required int robotX,
  required int robotY,
  required Set<Point> obstacles,
  required List<Point> ruta,
  required List<Map<String, dynamic>> posicionesProductos,
}) {
  // Área máxima para el mapa
  final double alturaMaxMapa = MediaQuery.of(context).size.height * 0.4;
  final double anchoMaxMapa = MediaQuery.of(context).size.width * 0.9;

  // Calcula el tamaño de celda para que el grid entero siempre quepa
  final double anchoCelda = anchoMaxMapa / anchoMapa;
  final double altoCelda = alturaMaxMapa / largoMapa;
  final double tamanyoCelda = anchoCelda < altoCelda ? anchoCelda : altoCelda;

  // Tamaño real del grid (ajustado para que quepan todas las filas/columnas)
  final double anchoReal = tamanyoCelda * anchoMapa;
  final double altoReal = tamanyoCelda * largoMapa;

  return Center(
    child: Container(
      // Marco negro alrededor
      padding: const EdgeInsets.all(6),
      decoration: BoxDecoration(
        color: Colors.black,
        borderRadius: BorderRadius.circular(12),
      ),
      width: anchoReal,
      height: altoReal,
      child: GridView.builder(
        physics: const NeverScrollableScrollPhysics(),
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: anchoMapa,
          childAspectRatio: 1,
        ),
        itemCount: anchoMapa * largoMapa,
        itemBuilder: (context, index) {
          int x = index % anchoMapa;
          int y = index ~/ anchoMapa;
          Point p = Point(x, y);

          Color color = Colors.white;
          Widget? content;

          if (p.x == robotX && p.y == robotY) {
            color = Colors.blue;
          } else if (obstacles.contains(p)) {
            color = Colors.black;
          } else if (ruta.contains(p)) {
            color = Colors.red;
          } 
          // Dibuja el producto si está en la posición correspondiente
          else if (posicionesProductos.any((prod) => prod["punto"] == p)) {
            color = Colors.green;
            final producto = posicionesProductos.firstWhere((prod) => prod["punto"] == p);
            content = Center(
              child: Text(
                producto["emoji"] ?? "❓",
                style: const TextStyle(fontSize: 18, color: Colors.white),
              ),
            );
          }

          return Container(
            decoration: BoxDecoration(
              color: color,
              border: Border.all(color: Colors.grey.shade300),
            ),
            child: content,
          );
        },
      ),
    ),
  );
}

/*
/// 🗺️ Grid de supermercat
Widget _buildMapa(BuildContext context) 
{
  // Área máxima para el mapa
  final double alturaMaxMapa = MediaQuery.of(context).size.height * 0.4;
  final double anchoMaxMapa = MediaQuery.of(context).size.width * 0.9;

  // Calcula el tamaño de celda para que el grid entero siempre quepa
  final double anchoCelda = anchoMaxMapa / anchoMapa;
  final double altoCelda = alturaMaxMapa / largoMapa;
  final double tamanyoCelda = anchoCelda < altoCelda ? anchoCelda : altoCelda;

  // Tamaño real del grid (ajustado para que quepan todas las filas/columnas)
  final double anchoReal = tamanyoCelda * anchoMapa;
  final double altoReal = tamanyoCelda * largoMapa;

  return Center(
    child: Container(
      // Marco negro alrededor
      padding: const EdgeInsets.all(6),
      decoration: BoxDecoration(
        color: Colors.black,
        borderRadius: BorderRadius.circular(12),
      ),
      // El tamaño del grid es SIEMPRE exactamente el que cabe en el área máxima, nunca mayor
      width: anchoReal,
      height: altoReal,
      child: GridView.builder(
        physics: const NeverScrollableScrollPhysics(),
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: anchoMapa,
          childAspectRatio: 1,
        ),
        itemCount: anchoMapa * largoMapa,
        itemBuilder: (context, index) {
          int x = index % anchoMapa;
          int y = index ~/ anchoMapa;
          Point p = Point(x, y);

          Color color = Colors.white;
          Widget? content;

          if (p.x == robotX && p.y == robotY) {
            color = Colors.blue;
          } else if (obstacles.contains(p)) {
            color = Colors.black;
          /*} else if (alimentsDisponibles.any((a) => a.coordenada == p)) {
            color = Colors.green;
            final aliment = alimentsDisponibles.firstWhere((a) => a.coordenada == p);
            content = Center(
              child: Icon(aliment.icona, color: Colors.white, size: 16),
            );*/
          } else if (ruta.contains(p)) {
            color = Colors.red;
          }
          return Container(
            decoration: BoxDecoration(
              color: color,
              border: Border.all(color: Colors.grey.shade300),
            ),
            child: content,
          );
        },
      ),
    ),
  );
}
*/