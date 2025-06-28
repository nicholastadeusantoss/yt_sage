from yt_sage.downloader import baixar_audio_youtube
from yt_sage.transcriber import transcrever_audio
from yt_sage.rag_chat import consultar_openai

def main():
    url = input("Cole o link do vídeo do YouTube: ")
    audio_path = baixar_audio_youtube(url)
    print("Transcrevendo com Faster-Whisper...")
    texto = transcrever_audio(audio_path)

    while True:
        pergunta = input("\nSua pergunta sobre o vídeo (ou 'sair'): ")
        if pergunta.lower() == "sair":
            break
        resposta = consultar_openai(texto, pergunta)
        print("\nResposta:\n", resposta)