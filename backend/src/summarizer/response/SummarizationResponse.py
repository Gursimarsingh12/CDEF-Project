from pydantic import BaseModel

class SummarizationResponse(BaseModel):
    summary: str