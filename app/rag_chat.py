import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_consulter(contexto: str, pergunta: str) -> str:
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You're a Youtube assistant, I'll ask questions about the context of the video"},
            {"role": "user", "content": f"Contexto: {contexto}\nPergunta: {pergunta}"}
        ]
    )
    return resposta.choices[0].message.content