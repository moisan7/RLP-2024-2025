import 'package:flutter/material.dart';
import 'screens/ruta_mapa_screen.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:collection';
import 'dart:convert';
import './models/aliment.dart';
// MIRAR
import 'package:http/http.dart' as http;

import 'package:avatar_glow/avatar_glow.dart';
import 'package:highlight_text/highlight_text.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;


void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'COMPA COMPRA APP',
      home: PantallaPrincipal(), // Aquí va tu widget con toda la lógica
      debugShowCheckedModeBanner: false,
    );
  }
}

/*
class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}
*/
class PantallaPrincipal extends StatefulWidget {
  @override
  _PantallaPrincipalState createState() => _PantallaPrincipalState();
}

class _PantallaPrincipalState extends State<PantallaPrincipal>  {
  int anchoMapa = 5;
  int largoMapa = 5;
  Set<Point> obstacles = {};

  static const int gridSize = 20;
  int robotX = 0;
  int robotY = 0;
  /// LLISTA ALIMENTS DISPONIBLES
  List<Aliment> alimentsDisponibles = [];


  final stt.SpeechToText _speech = stt.SpeechToText();
  bool _isListening = false;
  double _confidence = 1.0;

  String _recognizedText = '';

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) => print('onStatus: $val'),
        onError: (val) => print('onError: $val'),
      );
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) {
            setState(() {
              _recognizedText = val.recognizedWords.toLowerCase();
              if (val.hasConfidenceRating && val.confidence > 0) {
                _confidence = val.confidence;
              }
              _processVoiceInput(_recognizedText);
            });
          },
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
    }
  }

  void _processVoiceInput(String input) {
    input = input.toLowerCase();

    for (Aliment aliment in alimentsDisponibles) {
      final nomMinuscules = aliment.nom.toLowerCase();

      if (input.contains(nomMinuscules) &&
          !llistaFinal.any((item) => item.aliment.nom.toLowerCase() == nomMinuscules)) {
        setState(() {
          llistaFinal.add(AlimentSeleccionat(aliment: aliment, quantitat: 1));
          debugPrint("✅ Afegit per veu: ${aliment.nom}");
        });
      }
    }
  }

  /*void _processVoiceInput(String input) {
      for (String item in _availableItems) {
        if (input.contains(item) && !_shoppingList.contains(item)) {
          _shoppingList.add(item);
        }
      }
    }
    void _addItem(String item) {
    setState(() {
      if (!_shoppingList.contains(item)) {
        _shoppingList.add(item);
      }
    });
  }*/

// ==========================================================================
// ==                      ☁️ CLOUD FUNCTIONS ☁️                          ==
// ==========================================================================
  Future<void> getNombresProductosBD() async {
    final url = Uri.parse(
      "https://europe-west1-compacompraapp.cloudfunctions.net/getNombresProductosBD",
    );

    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final List nombres = data['nombres'];

        setState(() {
          alimentsDisponibles = nombres.map<Aliment>((nom) {
            return Aliment(
              nom: nom,
              icona: iconosPorNombre[nom] ?? "❓",
              coordenada: const Point(0, 0),  
            );
          }).toList();
        });
      } else {
        debugPrint("Error HTTP: ${response.statusCode}");
        debugPrint("Cuerpo: ${response.body}");
      }
    } catch (e) {
      debugPrint("Error al hacer la solicitud: $e");
    }
  }

  Future<void> consultarMapaBD() async {
    // URL de tu Cloud Function
    var url = Uri.parse("https://europe-west1-compacompraapp.cloudfunctions.net/consultarMapaBD");

    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        // Decodifica el JSON recibido
        final data = jsonDecode(response.body);

        // Lee ancho y largo del mapa
        int nuevoAncho = data['ancho'];
        int nuevoLargo = data['largo'];

        // Lee y transforma la lista de obstáculos
        Set<Point> nuevosObstacles = {};
        for (var obs in data['obstaculos']) {
          nuevosObstacles.add(Point(obs['x'], obs['y']));
        }

        // Actualiza el estado del widget para reflejar los cambios en la UI
        setState(() {
          anchoMapa = nuevoAncho;
          largoMapa = nuevoLargo;
          obstacles = nuevosObstacles;
        });
      } else {
        print("Error HTTP: ${response.statusCode}");
        print("Respuesta: ${response.body}");
      }
    } catch (e) {
      print("Error en la solicitud: $e");
    }
  }

  Future<void> consultarNombresBD() async {
    // Prepara la lista de nombres que tienes en tu llistaFinal
    final List<String> nombres = (llistaFinal.map((item) => item.aliment.nom)).toList().cast<String>();
    //final List<String> nombres = llistaFinal.map((item) => item.aliment.nom).toList();

    final url = Uri.parse("https://europe-west1-compacompraapp.cloudfunctions.net/consultarNombresBD");
    final payload = {
      "lista_nombres": nombres,
    };

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(payload),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        // Aquí depende de tu Cloud Function:
        // Supongamos que te devuelve algo como {"nombres_existentes": ["Leche", "Tomate"]}
        final List nombresExistentes = data["nombres_existentes"];

        setState(() {
          llistaFinal.removeWhere((item) => !nombresExistentes.contains(item.aliment.nom));
        });

        // Si quieres feedback visual, puedes usar un ScaffoldMessenger aquí para avisar al usuario
      } else {
        print("Error HTTP: ${response.statusCode}");
        print("Cuerpo: ${response.body}");
      }
    } catch (e) {
      print("Error al consultar nombres en la BD: $e");
    }
  }


// ==========================================================================
// ==                            VARIABLES                                 ==
// ==========================================================================
  late Map<String, String> iconosPorNombre;

  // Carga los iconos/emoji locales SOLO UNA VEZ
  Future<void> cargarIconosLocales() async {
    String jsonString = await rootBundle.loadString("iconos/icons.json");
    final Map<String, dynamic> jsonMap = jsonDecode(jsonString);

    iconosPorNombre = {
      for (var prod in jsonMap["productos"])
        prod["nombre"]: prod["emoji"]
    };
  }

  final Map<Aliment, int> quantitatsSeleccionades = {};
  final List<AlimentSeleccionat> llistaFinal = [];
  final List<Point> ruta = [];

  void afegirAliment(Aliment aliment) {
    final quantitat = quantitatsSeleccionades[aliment] ?? 0;
    if (quantitat > 0) {
      final existent = llistaFinal.indexWhere((a) => a.aliment.nom == aliment.nom);
      if (existent >= 0) {
        setState(() {
          llistaFinal[existent].quantitat += quantitat;
        });
      } else {
        setState(() {
          llistaFinal.add(AlimentSeleccionat(aliment: aliment, quantitat: quantitat));
        });
      }
      setState(() {
        quantitatsSeleccionades[aliment] = 0;
      });
    }
  }

  void calcularRutaRobot() {
    ruta.clear();
    Point actual = Point(robotX, robotY);

    for (final seleccionat in llistaFinal) {
      final dest = seleccionat.aliment.coordenada;
      Point? adjacent = trobarAdjacentLliure(dest);
      if (adjacent == null) continue;

      List<Point> cami = bfs(actual, adjacent);
      if (cami.isNotEmpty) {
        ruta.addAll(cami.skip(1));
        actual = adjacent;
      }
    }
    setState(() {});
  }

  Point? trobarAdjacentLliure(Point p) {
    final possibles = [
      Point(p.x + 1, p.y),
      Point(p.x - 1, p.y),
      Point(p.x, p.y + 1),
      Point(p.x, p.y - 1),
    ];
    for (final adj in possibles) {
      if (_valid(adj)) return adj;
    }
    return null;
  }

  bool _valid(Point p) {
    return p.x >= 0 && p.y >= 0 && p.x < gridSize && p.y < gridSize && !obstacles.contains(p);
  }

  List<Point> bfs(Point start, Point goal) {
    Queue<List<Point>> queue = Queue();
    Set<Point> visited = {};

    queue.add([start]);
    visited.add(start);

    while (queue.isNotEmpty) {
      final path = queue.removeFirst();
      final current = path.last;

      if (current == goal) return path;

      for (final dir in [
        Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1),
      ]) {
        final next = Point(current.x + dir.x, current.y + dir.y);
        if (_valid(next) && !visited.contains(next)) {
          visited.add(next);
          queue.add([...path, next]);
        }
      }
    }
    return [];
  }


// ==========================================================================
// ==                              WIDGETS                                 ==
// ==========================================================================
  /// 🛒 Llista d’aliments disponibles amb botons
  /// /// 🛒 Llista d’aliments disponibles amb botons (solo check)
    Widget _buildLlistaAliments(BuildContext context) {
    final alturaPantalla = MediaQuery.of(context).size.height;

    return SizedBox(
      height: alturaPantalla * 0.3,
      child: ListView.builder(
        itemCount: alimentsDisponibles.length,
        itemBuilder: (context, index) {
          final aliment = alimentsDisponibles[index];
          final yaEnLista = llistaFinal.any((item) => item.aliment.nom == aliment.nom);
          return ListTile(
            leading: aliment.icona.isNotEmpty
                ? Text(aliment.icona, style: TextStyle(fontSize: 24))
                : Icon(Icons.fastfood), // O cualquier icono Material por defecto
            title: Text(aliment.nom),
            trailing: IconButton(
              icon: Icon(
                Icons.check,
                color: yaEnLista ? Colors.green : null,
              ),
              onPressed: yaEnLista
                  ? null
                  : () {
                      setState(() {
                        llistaFinal.add(AlimentSeleccionat(aliment: aliment, quantitat: 1));
                      });
                    },
            ),
          );
        },
      ),
    );
  }


  /// 📦 Llista final d’aliments seleccionats
  /// Funcion que revisa que los productos estén correctos
  Widget _buildLlistaFinal() {
    return ListView.builder(
      itemCount: llistaFinal.length,
      itemBuilder: (context, index) {
        final item = llistaFinal[index];
        return ListTile(
          leading: item.aliment.icona.isNotEmpty
              ? Text(item.aliment.icona, style: TextStyle(fontSize: 24))
              : Icon(Icons.fastfood), // Fallback si no hay emoji
          title: Text(item.aliment.nom),
          trailing: IconButton(
            icon: const Icon(Icons.close, color: Colors.red),
            tooltip: 'Eliminar de la lista',
            onPressed: () {
              setState(() {
                llistaFinal.removeAt(index);
              });
            },
          ),
        );
      },
    );
  }

// ==========================================================================
// ==                            INICIAR ESTADO                            ==
// ==========================================================================

  @override
  void initState() {
    super.initState();
    _cargarTodo();
  }

  Future<void> _cargarTodo() async {
    try {
      await cargarIconosLocales();
      await getNombresProductosBD();
      await consultarMapaBD();
    } catch (e) {
      print('❌ Error al cargar recursos: $e');
      // Muestra un snackbar, alerta o lo que quieras
    }
  }



// ==========================================================================
// ==                               PANTALLA                               ==
// ==========================================================================
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        


      floatingActionButton: AvatarGlow(
        animate: _isListening,
        glowColor: Theme.of(context).primaryColor,
        endRadius: 75.0,
        duration: Duration(seconds: 2000),
        repeatPauseDuration: Duration(seconds: 1000),
        repeat: true,
        child: FloatingActionButton(
          onPressed: _listen,
          child: Icon(_isListening ? Icons.mic : Icons.mic_none),
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,





        appBar: AppBar(
          backgroundColor: Colors.orange[400],
          title: const Text(
            'COMPA COMPRA APP',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20, color: Colors.black),
          ),
          centerTitle: true,
          elevation: 0,
        ),
        body: Column(
          children: [
            // Parte de productos disponibles
            Expanded(
              flex: 1,
              child: Container(
                color: Colors.white,
                child: Column(
                  children: [
                    const Padding(
                      padding: EdgeInsets.symmetric(vertical: 12.0, horizontal: 16),
                      child: Align(
                        alignment: Alignment.centerLeft,
                        child: Text(
                          "🛒 PRODUCTOS DISPONIBLES",
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    Expanded(child: _buildLlistaAliments(context)),
                  ],
                ),
              ),
            ),




            // Parte de lista de la compra + botón validar (esto es lo que te he pasado)
            Expanded(
              flex: 1,
              child: Container(
                color: Colors.orange[200],  // Fondo naranja claro
                child: Column(
                  children: [
                    const Padding(
                      padding: EdgeInsets.symmetric(vertical: 12.0, horizontal: 16),
                      child: Align(
                        alignment: Alignment.centerLeft,
                        child: Text(
                          "📃 TU LISTA DE LA COMPRA",
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    Expanded(child: _buildLlistaFinal()),

                    // --- Botón Validar lista ---
                    Padding(
                      padding: const EdgeInsets.all(12.0),
                      child: SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          icon: const Icon(Icons.check_circle_outline, color: Colors.white),
                          label: const Text(
                            "Planificar ruta",
                            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.deepOrange[400],
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          onPressed: llistaFinal.isEmpty
                              ? null
                              : () {
                                  calcularRutaRobot(); // Calcula la ruta antes de navegar
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => RutaScreen(
                                        llistaFinal: llistaFinal,    // <<< ¡NO List.from()!
                                        ruta: ruta,                  // <<< ¡NO List.from()!
                                        anchoMapa: anchoMapa,
                                        largoMapa: largoMapa,
                                        obstacles: obstacles,
                                        robotX: robotX,
                                        robotY: robotY,
                                      ),
                                    ),
                                  ).then((_) {
                                    setState(() {}); // Así refrescas la pantalla principal al volver
                                  });
                                },
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
