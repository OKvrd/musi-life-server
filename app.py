from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['GET'])
def convert_audio():
    youtube_url = request.args.get('url')
    if not youtube_url:
        return jsonify({'error': 'Falta el enlace'}), 400
    
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['tv_embedded', 'mweb']
                }
            },
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info.get('url')
            if not audio_url and 'formats' in info:
                for f in info['formats']:
                    if f.get('url') and f.get('acodec') != 'none':
                        audio_url = f['url']
                        break
                        
        if not audio_url:
            return jsonify({'error': 'No se pudo extraer el audio'}), 500
            
        return jsonify({'url': audio_url})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
