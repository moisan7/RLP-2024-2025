import firebase_admin
from firebase_admin import firestore
import functions_framework
from flask import jsonify

firebase_admin.initialize_app()
db = firestore.client()

@functions_framework.http
def getNombresProductosBD(request):
    if request.method != 'GET':
        return jsonify({'error': 'Método no permitido, usa GET'}), 405
    try:
        productos_ref = db.collection('productos')
        docs = productos_ref.stream()
        nombres = []
        for doc in docs:
            data = doc.to_dict()
            if "nombre" in data:
                nombres.append(data["nombre"])
        return jsonify({'nombres': nombres})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
