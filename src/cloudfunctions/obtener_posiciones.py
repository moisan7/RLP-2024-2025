import firebase_admin
from firebase_admin import firestore
import functions_framework
from flask import jsonify, request

firebase_admin.initialize_app()
db = firestore.client()

@functions_framework.http
def obtenerPosicionesBD(request):
    if request.method != 'POST':
        return jsonify({'error': 'Método no permitido, usa POST'}), 405
    request_json = request.get_json(silent=True)
    if not request_json or 'lista_nombres' not in request_json:
        return jsonify({'error': 'Falta lista_nombres en el cuerpo de la petición'}), 400
    lista_nombres = request_json['lista_nombres']
    productos_ref = db.collection('productos')
    docs = productos_ref.stream()
    posiciones_dict = {}
    for doc in docs:
        data = doc.to_dict()
        nombre = data.get('nombre')
        posicion = data.get('posicion')
        if nombre and posicion and 'x' in posicion and 'y' in posicion:
            posiciones_dict[nombre] = {'x': posicion['x'], 'y': posicion['y']}
    posiciones = []
    for nombre in lista_nombres:
        if nombre in posiciones_dict:
            posiciones.append(posiciones_dict[nombre])
        else:
            posiciones.append(None)
    return jsonify({'posiciones': posiciones})
