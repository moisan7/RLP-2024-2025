from google.cloud import speech
from google.cloud import language_v1
import base64
import tempfile
import functions_framework

@functions_framework.http
def procesar_lista_de_la_compra(request):
    if request.method != 'POST':
        return ('Only POST allowed', 405)
    data = request.get_json()
    if not data or 'audio' not in data:
        return ('Missing audio data', 400)
    audio_content = base64.b64decode(data['audio'])
    with tempfile.NamedTemporaryFile(suffix=".flac") as temp_audio:
        temp_audio.write(audio_content)
        temp_audio.seek(0)
        speech_client = speech.SpeechClient()
        with open(temp_audio.name, "rb") as f:
            audio = speech.RecognitionAudio(content=f.read())
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            language_code="es-ES"
        )
        response = speech_client.recognize(config=config, audio=audio)
        transcript = " ".join([r.alternatives[0].transcript for r in response.results])
    if not transcript.strip():
        return {'transcript': '', 'productos': [], 'es_lista_valida': False}
    language_client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=transcript,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="es"
    )
    entities_response = language_client.analyze_entities(document=document)
    productos = []
    for entity in entities_response.entities:
        if language_v1.Entity.Type(entity.type_).name == 'CONSUMER_GOOD':
            productos.append(entity.name.lower())
    productos = list(set(productos))
    es_lista_valida = len(productos) >= 1
    return {
        'transcript': transcript,
        'productos': productos,
        'es_lista_valida': es_lista_valida
    }
