import firebase_admin
from firebase_admin import firestore
import functions_framework
from flask import jsonify, request

firebase_admin.initialize_app()
db = firestore.client()

@functions_framework.http
def consultarMapaBD(request):
    if request.method != 'GET':
        return jsonify({'error': 'Método no permitido, usa GET'}), 405
    try:
        dimensiones_ref = db.collection('mapa').document('dimensiones')
        dimensiones_doc = dimensiones_ref.get()
        if not dimensiones_doc.exists:
            return jsonify({'error': "No se encontró el documento de dimensiones del mapa."}), 404
        dimensiones = dimensiones_doc.to_dict()
        ancho = dimensiones.get('ancho')
        largo = dimensiones.get('largo')
        if ancho is None or largo is None:
            return jsonify({'error': "El documento de dimensiones no contiene 'ancho' o 'largo'."}), 400
        obstaculos_ref = db.collection('obstaculos')
        obstaculos_docs = obstaculos_ref.stream()
        posiciones_obstaculos = []
        for doc in obstaculos_docs:
            data = doc.to_dict()
            x = data.get('x')
            y = data.get('y')
            if x is not None and y is not None:
                posiciones_obstaculos.append({'x': x, 'y': y})
        return jsonify({
            'ancho': ancho,
            'largo': largo,
            'obstaculos': posiciones_obstaculos
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
