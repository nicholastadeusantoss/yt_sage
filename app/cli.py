import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.schema import Document

from app.downloader import yt_audio_download
from app.transcriber import audio_transcriber
from app.rag_chat import ai_consulter


def main():
    # Carrega as variáveis de ambiente
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Lê o transcript como um documento
    url = input("Paste the YouTube video link: ")
    
    audio_path = yt_audio_download(url)
    
    #print("Transcribing with Faster-Whisper...")
    
    texto = audio_transcriber(audio_path)

    loader = TextLoader(texto)
    docs = [Document(page_content=texto)]

    # Cria embedding e banco vetorial
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Define LLM e pipeline de QA com RAG
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Pergunta do usuário
    while True:
        query = input("Sua pergunta sobre o vídeo (ou 'sair'): ")
        if query.lower() == "sair":
            break

        result = qa_chain(query)
        print("\nResposta:")
        print(result["result"])