from unittest.mock import patch
from yt_sage import rag_chat

@patch("yt_sage.rag_chat.client.chat.completions.create")
def test_consultar_ai(mock_create):
    mock_create.return_value.choices = [type("msg", (), {"message": type("m", (), {"content": "Mock answer"})()})()]
    answer = rag_chat.ai_consulter("video text", "What is the subject?")
    assert "Mock answer" in answer