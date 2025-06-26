import firebase_admin
from firebase_admin import firestore
import functions_framework
from flask import jsonify, request

firebase_admin.initialize_app()
db = firestore.client()

@functions_framework.http
def consultarNombresBD(request):
    if request.method != 'POST':
        return jsonify({'error': 'Método no permitido, usa POST'}), 405
    request_json = request.get_json(silent=True)
    if not request_json or 'lista_nombres' not in request_json:
        return jsonify({'error': 'Falta lista_nombres en el cuerpo de la petición'}), 400
    lista_nombres = request_json['lista_nombres']
    productos_ref = db.collection('productos')
    docs = productos_ref.stream()
    nombres_en_bd = set()
    for doc in docs:
        data = doc.to_dict()
        if "nombre" in data:
            nombres_en_bd.add(data["nombre"])
    coincidencias = [nombre for nombre in lista_nombres if nombre in nombres_en_bd]
    return jsonify({'coincidencias': coincidencias})
