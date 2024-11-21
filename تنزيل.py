from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

# إنشاء مجلد التحميلات
DOWNLOAD_FOLDER = "/tmp/downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    return '''
        <h1>Video Downloader</h1>
        <form action="/download" method="post">
            <input type="text" name="url" placeholder="Enter video URL" required>
            <button type="submit">Download</button>
        </form>
    '''

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return "Error: No URL provided.", 400

    try:
        # تحميل الفيديو
        command = ["yt-dlp", "-o", f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s", url]
        subprocess.run(command, check=True)
        return f"Download complete! Video saved to temporary folder."
    except subprocess.CalledProcessError:
        return "Error: Failed to download video.", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)