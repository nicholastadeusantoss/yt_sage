import os
from unittest.mock import patch
from yt_sage.downloader import yt_audio_download

@patch("yt_sage.downloader.YoutubeDL")
def test_yt_audio_download(mock_ytdl):
    fake_audio_path = "/tmp/video.mp3"

    instance = mock_ytdl.return_value.__enter__.return_value
    instance.extract_info.return_value = {"title": "video"}
    instance.prepare_filename.return_value = fake_audio_path.replace(".mp3", ".webm")

    audio_path = yt_audio_download("https://youtube.com/fake")
    assert audio_path.endswith(".mp3")
