import 'package:flutter/material.dart';
import '../models/aliment.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class RutaScreen extends StatefulWidget {
  final List<AlimentSeleccionat> llistaFinal;
  final List<Point> ruta;
  final int anchoMapa;
  final int largoMapa;
  final Set<Point> obstacles;
  final int robotX;
  final int robotY;

  const RutaScreen({
    Key? key,
    required this.llistaFinal,
    required this.ruta,
    required this.anchoMapa,
    required this.largoMapa,
    required this.obstacles,
    required this.robotX,
    required this.robotY,
  }) : super(key: key);

  @override
  State<RutaScreen> createState() => _RutaScreenState();
}

class _RutaScreenState extends State<RutaScreen> {
  // Productos con nombre, punto y emoji
  List<Map<String, dynamic>> posicionesProductos = [];

  @override
  void initState() {
    super.initState();
    _obtenerPosicionesBD();
  }

  Future<void> _obtenerPosicionesBD() async {
    final nombres = widget.llistaFinal.map((item) => item.aliment.nom).toList();
    final url = Uri.parse("https://europe-west1-compacompraapp.cloudfunctions.net/obtenerPosicionesBD");
    final payload = {"lista_nombres": nombres};

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(payload),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final posiciones = data["posiciones"] as List;

        // Monta la lista de productos con coordenadas y emoji
        List<Map<String, dynamic>> productos = [];
        for (int i = 0; i < posiciones.length; i++) {
          final pos = posiciones[i];
          if (pos == null) continue; // Saltar productos no encontrados
          final nombre = nombres[i];
          final emoji = _buscarEmojiPorNombre(nombre);

          productos.add({
            "nombre": nombre,
            "punto": Point(pos["x"], pos["y"]),
            "emoji": emoji,
          });
        }
        setState(() {
          posicionesProductos = productos;
        });
      } else {
        print("Error HTTP: ${response.statusCode}");
        print("Respuesta: ${response.body}");
      }
    } catch (e) {
      print("Error al hacer la solicitud: $e");
    }
  }

  

  // Busca el emoji a partir del nombre usando llistaFinal (o una lista local de todos los alimentos)
  String _buscarEmojiPorNombre(String nombre) {
    try {
      final aliment = widget.llistaFinal.firstWhere((a) => a.aliment.nom == nombre).aliment;
      return aliment.icona.isNotEmpty ? aliment.icona : "❓";
    } catch (e) {
      return "❓";
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ruta del Robot')),
      body: Column(
        children: [
          _buildLlistaCompra(),
          const Divider(),
          Expanded(child: _buildMapa(context)),
        ],
      ),
    );
  }

  Widget _buildLlistaCompra() {
    if (widget.llistaFinal.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(16),
        child: Text(
          "No has seleccionado ningún producto.",
          style: TextStyle(color: Colors.grey),
        ),
      );
    }
    return Container(
      color: Colors.grey[100],
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Wrap(
        spacing: 12,
        runSpacing: 8,
        children: widget.llistaFinal.map((item) {
          return Chip(
            avatar: item.aliment.icona.isNotEmpty
                ? Text(item.aliment.icona, style: const TextStyle(fontSize: 20))
                : const Icon(Icons.fastfood, size: 18),
            label: Text(item.aliment.nom),
            labelPadding: const EdgeInsets.symmetric(horizontal: 8),
            backgroundColor: Colors.white,
          );
        }).toList(),
      ),
    );
  }

  Widget _buildMapa(BuildContext context) {
    final double alturaMaxMapa = MediaQuery.of(context).size.height * 0.45;
    final double anchoMaxMapa = MediaQuery.of(context).size.width * 0.95;
    final double anchoCelda = anchoMaxMapa / widget.anchoMapa;
    final double altoCelda = alturaMaxMapa / widget.largoMapa;
    final double tamanyoCelda = anchoCelda < altoCelda ? anchoCelda : altoCelda;
    final double anchoReal = tamanyoCelda * widget.anchoMapa;
    final double altoReal = tamanyoCelda * widget.largoMapa;

    return Center(
      child: Container(
        margin: const EdgeInsets.only(top: 8, bottom: 18),
        padding: const EdgeInsets.all(6),
        decoration: BoxDecoration(
          color: Colors.black,
          borderRadius: BorderRadius.circular(14),
        ),
        width: anchoReal,
        height: altoReal,
        child: GridView.builder(
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: widget.anchoMapa,
            childAspectRatio: 1,
          ),
          itemCount: widget.anchoMapa * widget.largoMapa,
          itemBuilder: (context, index) {
            int x = index % widget.anchoMapa;
            int y = index ~/ widget.anchoMapa;
            Point p = Point(x, y);

            Color color = Colors.white;
            Widget? content;

            if (p.x == widget.robotX && p.y == widget.robotY) {
              color = Colors.blue;
            } else if (widget.obstacles.contains(p)) {
              color = Colors.black;
            } else if (widget.ruta.contains(p)) {
              color = Colors.red;
            } 
            // Productos seleccionados en sus posiciones reales desde la Cloud Function
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
}
