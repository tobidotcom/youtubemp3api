from flask import Flask, request, jsonify
import yt_dlp
import logging
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/convert', methods=['POST'])
def convert_youtube_to_mp3():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    retries = 3
    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return jsonify({'message': 'Conversion successful', 'file': 'audio.mp3'}), 200
        except yt_dlp.utils.DownloadError as e:
            logger.error(f"Download error: {e}")
            if '403' in str(e) or '503' in str(e):
                if attempt < retries - 1:
                    logger.info(f"Retrying ({attempt + 1}/{retries})...")
                    time.sleep(5)
                else:
                    return jsonify({'error': 'Failed to download video after multiple attempts.'}), 500
            else:
                return jsonify({'error': str(e)}), 500
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

