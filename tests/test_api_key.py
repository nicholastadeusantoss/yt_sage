from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # carrega o .env

def test_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Variável OPENAI_API_KEY não encontrada.")
        return

    client = OpenAI(api_key=api_key)

    try:
        response = client.models.list()
        print("Chave API válida! Modelos disponíveis:")
        for model in response.data:
            print(model.id)
    except Exception as e:
        print(f"Erro ao acessar a API OpenAI: {e}")

if __name__ == "__main__":
    test_openai_api_key()
