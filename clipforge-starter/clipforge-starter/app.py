from pathlib import Path
from uuid import uuid4
import math
import re
import subprocess

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge

ROOT = Path(__file__).resolve().parent
UPLOADS = ROOT / 'uploads'
CLIPS = ROOT / 'clips'
UPLOADS.mkdir(exist_ok=True)
CLIPS.mkdir(exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024  # 512 MB local demo limit
ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.mkv'}

@app.get('/')
def index():
    return render_template('index.html')

@app.errorhandler(RequestEntityTooLarge)
def too_large(_error):
    return jsonify(error='The video is too large for this demo (512 MB maximum).'), 413

@app.post('/api/clip')
def create_clip():
    video = request.files.get('video')
    if not video or not video.filename:
        return jsonify(error='Please select a video first.'), 400
    extension = Path(video.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify(error='Choose an MP4, MOV, or MKV video.'), 400

    try:
        start = float(request.form.get('start', '0'))
        duration = float(request.form.get('duration', '30'))
    except (TypeError, ValueError):
        return jsonify(error='Start time and length must be numbers.'), 400

    if not math.isfinite(start) or not 0 <= start <= 7200:
        return jsonify(error='Start time must be between 0 and 7200 seconds.'), 400
    if not math.isfinite(duration) or not 5 <= duration <= 60:
        return jsonify(error='Clip length must be between 5 and 60 seconds.'), 400

    job_id = uuid4().hex
    input_file = UPLOADS / f'{job_id}{extension}'
    output_file = CLIPS / f'{job_id}.mp4'
    try:
        video.save(input_file)
        # Center-crop to 9:16. Smart tracking and highlight detection come later.
        command = [
            'ffmpeg', '-nostdin', '-y', '-hide_banner', '-loglevel', 'error',
            '-ss', str(start), '-i', str(input_file), '-t', str(duration),
            '-vf', 'scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart',
            str(output_file),
        ]
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=900)
    except FileNotFoundError:
        return jsonify(error='FFmpeg was not found. Install it and add it to PATH.'), 500
    except subprocess.TimeoutExpired:
        return jsonify(error='Processing took too long. Try a shorter video.'), 500
    except subprocess.CalledProcessError:
        return jsonify(error='FFmpeg could not process this video. Check that it plays normally.'), 400
    finally:
        input_file.unlink(missing_ok=True)

    if not output_file.exists() or output_file.stat().st_size == 0:
        return jsonify(error='No clip was generated. Check your start time.'), 400
    return jsonify(download_url=f'/download/{job_id}', message='Clip created successfully!')

@app.get('/download/<job_id>')
def download(job_id):
    if not re.fullmatch(r'[a-f0-9]{32}', job_id):
        return jsonify(error='Invalid clip ID.'), 404
    return send_from_directory(CLIPS, f'{job_id}.mp4', as_attachment=True, download_name='short.mp4')

if __name__ == '__main__':
    # LOCAL DEVELOPMENT ONLY. Do not expose this server publicly.
    app.run(host='127.0.0.1', port=5000, debug=False)
