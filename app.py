from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_youtube_to_mp3():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # yt-dlp options to download audio directly in MP3 format
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Assume the file is named audio.mp3
        output_file = "audio.mp3"

        # Return success response
        return jsonify({'message': 'Conversion successful', 'file': output_file}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
