# ClipForge — Your own locally run video-clipping website

This is a **working beginner starter** built with HTML, CSS, JavaScript, Flask and FFmpeg. **No website builder is involved.**

## Current features
- Upload MP4, MOV, or MKV (up to 512 MB)
- Choose the start time and duration (5–60 seconds)
- Produce a center-cropped 720×1280 vertical MP4
- Download the finished clip

**Important:** This starter does NOT yet automatically find exciting moments or use AI. Add that after the video upload/cutting workflow works.

## Installation (Windows)
1. Install Python 3.11+ if needed.
2. Install FFmpeg separately, ensuring the `ffmpeg` command works in Command Prompt (`ffmpeg -version`).
3. Unzip this project and open Command Prompt or Windows Terminal inside the `clipforge-starter` folder.
4. Run:

    py -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt
    python app.py

5. Open `http://127.0.0.1:5000` in your browser.
6. Try uploading a small test MP4, enter start time 0 and length 15, then download the processed clip.
7. Stop the server with Ctrl+C.

## Files
- `app.py`: Flask web backend and FFmpeg processing
- `templates/index.html`: your webpage
- `static/style.css`: visual design
- `static/app.js`: browser upload and download interactions
- `clips/`: generated outputs (delete old clips to save disk space)
- `uploads/`: source files (removed automatically after processing)

## Upgrade roadmap
1. Add `faster-whisper` for timestamped transcripts.
2. Add a local Ollama model to rank highlight windows using dialogue, reactions, and other signals.
3. Pass chosen start/end times to the existing FFmpeg processing function.
4. Add on-video captions, preview and clip review tools.
5. Add a jobs queue and a database, then proper sign-in and per-user storage.
6. Before going public, add authentication, rate limits, verified media validation, upload security, background workers, quotas, and automatic cleanup. Use a production WSGI server, HTTPS, and a suitable hosting setup. Do **not** expose the bundled Flask development server directly to the internet.

## Reality check
- The website uses open-source tools but requires downloading/ installing Python libraries and FFmpeg.
- Local testing can be free. A public website needs a reachable server; a custom domain is optional, and hosting can have costs.
- Center-cropping can cut off subjects in horizontal gameplay; smart subject tracking is a later feature.
- Process only videos you have permission to use.
