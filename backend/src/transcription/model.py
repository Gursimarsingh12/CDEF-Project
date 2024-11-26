from typing import List
from fastapi import UploadFile
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC
from firebase_admin import credentials, initialize_app, storage
import torch
from datetime import datetime
import io
import librosa
from transcription.response.TranscriptionResponse import TranscriptionResponse
from auth.DatabaseController import getTranscriptionCollection
from config import Config

firebaseConfig = {
  "type": Config.FIREBASE_TYPE,
  "project_id": Config.FIREBASE_PROJECT_ID,
  "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
  "private_key": Config.FIREBASE_PRIVATE_KEY,
  "client_email": Config.FIREBASE_CLIENT_EMAIL,
  "client_id": Config.FIREBASE_CLIENT_ID,
  "auth_uri": Config.FIREBASE_AUTH_URI,
  "token_uri": Config.FIREBASE_TOKEN_URI,
  "auth_provider_x509_cert_url": Config.FIREBASE_AUTH_PROVIDER_CERT_URL,
  "client_x509_cert_url": Config.FIREBASE_CLIENT_CERT_URL,
  "universe_domain": Config.FIREBASE_UNIVERSE_DOMAIN
}

cred = credentials.Certificate(firebaseConfig)
initialize_app(cred, {"storageBucket": "usar-admin.appspot.com"})

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

async def process_audio_file(email: str, file: UploadFile) -> TranscriptionResponse:
    if not file.content_type.startswith("audio/"):
        raise ValueError("Invalid file type. Please upload an audio file.")
    audio_bytes = await file.read()
    file_link = upload_file_to_firebase(email, file.filename, audio_bytes, file.content_type)
    transcription = transcribe_audio(audio_bytes)
    metadata = {
        "email": email,
        "file_name": file.filename,
        "file_link": file_link,
        "transcription": transcription,
        "uploaded_at": datetime.now()
    }
    metadata_collection = await getTranscriptionCollection()
    metadata_collection.insert_one(metadata)
    return TranscriptionResponse(
        email=email,
        file_name=file.filename,
        file_link=file_link,
        transcription=transcription
    )
    
def upload_file_to_firebase(email: str, file_name: str, file_data: bytes, content_type: str) -> str:
    bucket = storage.bucket()
    storage_path = f"{email}/{file_name}"
    blob = bucket.blob(storage_path)
    blob.upload_from_string(file_data, content_type=content_type)
    return blob.public_url

def transcribe_audio(audio_bytes: bytes) -> str: 
    audio_stream = io.BytesIO(audio_bytes)
    speech, _ = librosa.load(audio_stream, sr=16000, mono=True)
    speech = librosa.util.normalize(speech)
    input_values = tokenizer(
        speech, return_tensors="pt", sampling_rate=16000).input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    return tokenizer.decode(predicted_ids[0])

async def getTranscriptions(email: str) -> List[TranscriptionResponse]:
    metadata_collection = await getTranscriptionCollection()
    transcriptions = metadata_collection.find({"email": email})
    return [TranscriptionResponse(**transcription) async for transcription in transcriptions]