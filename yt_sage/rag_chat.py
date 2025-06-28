import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def consultar_openai(contexto: str, pergunta: str) -> str:
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente de vídeos do YouTube."},
            {"role": "user", "content": f"Contexto: {contexto}\nPergunta: {pergunta}"}
        ]
    )
    return resposta.choices[0].message.content