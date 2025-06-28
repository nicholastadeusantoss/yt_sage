import os
from unittest.mock import patch
from yt_sage.downloader import baixar_audio_youtube

@patch("yt_sage.downloader.YoutubeDL")
def test_baixar_audio_youtube(mock_ytdl):
    fake_audio_path = "/tmp/video.mp3"

    instance = mock_ytdl.return_value.__enter__.return_value
    instance.extract_info.return_value = {"title": "video"}
    instance.prepare_filename.return_value = fake_audio_path.replace(".mp3", ".webm")

    audio_path = baixar_audio_youtube("https://youtube.com/fake")
    assert audio_path.endswith(".mp3")
