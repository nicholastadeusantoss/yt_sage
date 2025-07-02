from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.downloader import yt_audio_download
from app.transcriber import audio_transcriber
from app.rag_chat import create_qa_chain

app = FastAPI()
transcript_text = ""  # Guardar a transcrição em memória

class VideoURL(BaseModel):
    url: str

class UserQuestion(BaseModel):
    question: str

@app.post("/transcribe")
def transcribe_video(payload: VideoURL):
    global transcript_text
    audio_path = yt_audio_download(payload.url)
    transcript_text = audio_transcriber(audio_path)
    return {"message": "Transcrição realizada com sucesso."}

@app.post("/ask")
def ask_question(payload: UserQuestion):
    global transcript_text
    if not transcript_text:
        return {"detail": "Transcrição não encontrada. Faça /transcribe antes."}
    qa_chain = create_qa_chain(transcript_text)
    result = qa_chain(payload.question)
    answer = result["result"]
    return {"answer": answer}
