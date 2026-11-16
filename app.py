import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['GET'])
def convert_audio():
    youtube_url = request.args.get('url')
    if not youtube_url:
        return jsonify({'error': 'Falta el enlace'}), 400
    
    # Extraer el ID del video de YouTube de forma segura
    video_id = None
    if "v=" in youtube_url:
        video_id = youtube_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
        
    if not video_id:
        return jsonify({'error': 'URL inválida'}), 400
        
    try:
        # Consultar la API pública de Piped para obtener el stream de audio directo
        response = requests.get(f"https://pipedapi.kavin.rocks/streams/{video_id}", timeout=10)
        data = response.json()
        
        audio_streams = [s for s in data.get('audioStreams', []) if s.get('url')]
        if not audio_streams:
            return jsonify({'error': 'No se pudo extraer el audio'}), 500
            
        audio_url = audio_streams[0]['url']
        return jsonify({'url': audio_url})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
