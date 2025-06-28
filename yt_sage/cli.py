from yt_sage.downloader import yt_audio_download
from yt_sage.transcriber import audio_transcriber
from yt_sage.rag_chat import ai_consulter

def main():
    url = input("Paste the YouTube video link: ")
    audio_path = yt_audio_download(url)
    print("Transcribing with Faster-Whisper...")
    texto = audio_transcriber(audio_path)

    while True:
        pergunta = input("\nWhat is your question? (or type 'leave'): ")
        if pergunta.lower() == "leave":
            break
        resposta = ai_consulter(texto, pergunta)
        print("\Answer:\n", resposta)