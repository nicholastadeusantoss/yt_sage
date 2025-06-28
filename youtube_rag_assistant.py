import os
import shutil
import tempfile
from yt_dlp import YoutubeDL
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente (coloque sua OPENAI_API_KEY no .env)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Caminho do modelo Whisper
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

# Modelo de embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def baixar_audio_youtube(url):
    temp_dir = tempfile.mkdtemp()
    output_template = os.path.join(temp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        nome_base = ydl.prepare_filename(info).rsplit(".", 1)[0]
        caminho_mp3_temp = nome_base + ".mp3"

    # Move para a pasta do projeto
    caminho_final = os.path.join(os.getcwd(), "audio.mp3")
    shutil.move(caminho_mp3_temp, caminho_final)
    return caminho_final

def transcrever_audio(caminho_audio):
    print("Transcrevendo com Faster-Whisper...")
    segments, _ = whisper_model.transcribe(caminho_audio)
    texto = " ".join([segment.text for segment in segments])
    return texto

def dividir_em_trechos(texto, max_tokens=500):
    palavras = texto.split()
    trechos = []
    for i in range(0, len(palavras), max_tokens):
        trecho = " ".join(palavras[i:i+max_tokens])
        trechos.append(trecho)
    return trechos

def gerar_embeddings(trechos):
    return embedding_model.encode(trechos)

def consultar_openai(contexto, pergunta):
    prompt = f"""
Você é um assistente útil. Responda à pergunta com base no conteúdo abaixo extraído de um vídeo do YouTube:

Contexto:
\"\"\"
{contexto}
\"\"\"

Pergunta: {pergunta}
Resposta:
"""
    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content.strip()

def main():
    url = input("Cole o link do vídeo do YouTube: ")
    caminho_audio = baixar_audio_youtube(url)
    texto = transcrever_audio(caminho_audio)
    os.remove(caminho_audio)  # Limpa o mp3 após uso

    trechos = dividir_em_trechos(texto)
    embeddings = gerar_embeddings(trechos)

    while True:
        pergunta = input("\nSua pergunta sobre o vídeo (ou 'sair'): ")
        if pergunta.lower() == "sair":
            break
        pergunta_emb = embedding_model.encode([pergunta])
        similaridades = cosine_similarity(pergunta_emb, embeddings)[0]
        top_idx = similaridades.argmax()
        contexto = trechos[top_idx]

        resposta = consultar_openai(contexto, pergunta)
        print("\nResposta:", resposta)

if __name__ == "__main__":
    main()