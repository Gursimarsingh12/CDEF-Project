from pydantic import BaseModel

class SummarizationResponse(BaseModel):
    email: str
    text: str
    summary: str