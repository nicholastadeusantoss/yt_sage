from unittest.mock import patch
from yt_sage import rag_chat

@patch("yt_sage.rag_chat.client.chat.completions.create")
def test_consultar_openai(mock_create):
    mock_create.return_value.choices = [type("msg", (), {"message": type("m", (), {"content": "Resposta mockada"})()})()]
    resposta = rag_chat.consultar_openai("texto do vídeo", "o que é o assunto?")
    assert "Resposta mockada" in resposta