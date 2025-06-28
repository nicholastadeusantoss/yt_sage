from unittest.mock import patch
from yt_sage import transcriber

@patch("yt_sage.transcriber.model.transcribe")
def test_transcription(mock_transcribe):
    mock_transcribe.return_value = ([type("seg", (), {"text": "teste"})()], None)
    texto = transcriber.transcrever_audio("fake_path.mp3")
    assert "teste" in texto
