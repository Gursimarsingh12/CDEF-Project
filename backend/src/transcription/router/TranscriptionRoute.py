from typing import List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from transcription.model import getTranscriptions, process_audio_file
from transcription.response.TranscriptionResponse import TranscriptionResponse

transcription_router = APIRouter(
    prefix="/transcription",
    tags=["Transcription"],
    responses={404: {"description": "Not found"}}
)

@transcription_router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(email: str = Form(), file: UploadFile = File()):
    try:
        return await process_audio_file(email, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@transcription_router.get("/transcriptions", response_model=List[TranscriptionResponse])
async def get_transcriptions(email: str):
    try:
        return await getTranscriptions(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")