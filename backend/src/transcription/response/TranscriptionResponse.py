from datetime import datetime
from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    email: str
    file_name: str
    file_link: str
    transcription: str
    uploaded_at: datetime