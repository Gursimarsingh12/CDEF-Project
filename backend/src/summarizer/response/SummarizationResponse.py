from datetime import datetime
from pydantic import BaseModel

class SummarizationResponse(BaseModel):
    email: str
    text: str
    summary: str
    uploaded_at: datetime