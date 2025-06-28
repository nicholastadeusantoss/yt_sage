from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def audio_transcriber(audio_path: str) -> str:
    segments, _ = model.transcribe(audio_path)
    return " ".join(segment.text for segment in segments)
