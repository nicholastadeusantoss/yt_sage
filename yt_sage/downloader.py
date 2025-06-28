import os
import tempfile
from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename

def baixar_audio_youtube(url: str) -> str:
    temp_dir = tempfile.mkdtemp()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = sanitize_filename(info["title"])
        mp3_path = os.path.join(temp_dir, f"{title}.mp3")
        return mp3_path
