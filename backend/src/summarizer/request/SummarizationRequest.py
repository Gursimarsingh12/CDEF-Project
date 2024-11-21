from pydantic import BaseModel

class SummarizationRequest(BaseModel):
    text: str
    max_length: int = 100
    min_length: int = 25