from flask import Flask, request, jsonify
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_youtube_to_mp3():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Download the video
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_audio=True).first()
        video_file = video_stream.download(filename="video.mp4")

        # Convert to MP3
        audio = AudioSegment.from_file(video_file)
        output_file = "audio.mp3"
        audio.export(output_file, format="mp3")

        # Clean up the video file
        os.remove(video_file)

        # Return success response
        return jsonify({'message': 'Conversion successful', 'file': output_file}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
