from flask import Flask, request, jsonify
import yt_dlp
import os
import logging
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to your cookie file
COOKIE_FILE = 'cookies.txt'

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
            'no_warnings': True,
            'cookiefile': COOKIE_FILE,  # Path to your cookie file
        }

        retries = 3
        for attempt in range(retries):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                # Return success response
                return jsonify({'message': 'Conversion successful', 'file': 'audio.mp3'}), 200
            except yt_dlp.utils.DownloadError as e:
                logger.error(f"Download error: {e}")
                if '403' in str(e) or '503' in str(e):
                    # Handle potential CAPTCHA issues or temporary bans
                    if attempt < retries - 1:
                        logger.info(f"Retrying ({attempt + 1}/{retries})...")
                        time.sleep(5)  # Wait before retrying
                    else:
                        return jsonify({'error': 'Failed to download video after multiple attempts. Please check the URL or try again later.'}), 500
                else:
                    return jsonify({'error': str(e)}), 500
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

    except Exception as e:
        logger.error(f"General exception: {e}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
