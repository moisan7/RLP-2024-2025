import firebase_admin
from firebase_admin import firestore
import functions_framework
from flask import jsonify, request

firebase_admin.initialize_app()
db = firestore.client()

@functions_framework.http
def consultarCajaRegistradoraBD(request):
    if request.method != 'GET':
        return jsonify({'error': 'Método no permitido, usa GET'}), 405
    try:
        cajas_ref = db.collection('caja_registradora')
        cajas_docs = cajas_ref.stream()
        posiciones = []
        for doc in cajas_docs:
            data = doc.to_dict()
            x = data.get('x')
            y = data.get('y')
            if x is not None and y is not None:
                posiciones.append({'x': x, 'y': y})
        if not posiciones:
            return jsonify({'error': 'No se encontró ninguna caja registradora.'}), 404
        return jsonify({'cajas_registradoras': posiciones})
    except Exception as e:
        return jsonify({'error': str(e)}), 500