from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app) # Allows your GitHub Pages site to securely talk to this API

@app.route('/api/download', methods=['POST'])
def download_media():
    data = request.json
    url = data.get('url')
    requested_format = data.get('format', 'mp4')
    
    if not url:
        return jsonify({'success': False, 'error': 'No video link detected'})

    # Configure extraction parameters based on user selection
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }

    if requested_format == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Best combined video/audio or raw download
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(meta)
            
            # Adjust explicit extension naming if converted to MP3
            if requested_format == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'

        return jsonify({
            'success': True,
            'filename': os.path.basename(filename)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
