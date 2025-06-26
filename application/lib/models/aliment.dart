class Aliment {
  final String nom;
  final String icona;
  final Point coordenada;

  Aliment({
    required this.nom, 
    required this.icona, 
    required this.coordenada
  });
}

class AlimentSeleccionat {
  final Aliment aliment;
  int quantitat;

  AlimentSeleccionat({required this.aliment, required this.quantitat});
}

class Point {
  final int x;
  final int y;

  const Point(this.x, this.y);

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Point && runtimeType == other.runtimeType && x == other.x && y == other.y;

  @override
  int get hashCode => x.hashCode ^ y.hashCode;

  @override
  String toString() => '($x, $y)';
}