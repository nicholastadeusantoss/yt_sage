from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # carrega o .env

def test_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY variable not found.")
        return

    client = OpenAI(api_key=api_key)

    try:
        response = client.models.list()
        print("API Key is valid! Models:")
        for model in response.data:
            print(model.id)
    except Exception as e:
        print(f"Access error in the OpenAI API: {e}")

if __name__ == "__main__":
    test_openai_api_key()
