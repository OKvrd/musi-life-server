from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['GET'])
def convert_audio():
    youtube_url = request.args.get('url')
    if not youtube_url:
        return jsonify({'error': 'Falta el enlace'}), 400

    try:
        cmd = ['yt-dlp', '-g', '-f', 'bestaudio', youtube_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=50)
        
        audio_url = result.stdout.strip().split('\n')[0]
        
        if not audio_url:
            return jsonify({'error': 'No se pudo extraer el audio'}), 500

        return jsonify({'url': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
