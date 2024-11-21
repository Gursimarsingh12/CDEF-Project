from fastapi import APIRouter, HTTPException, status, Header, Query
from summarizer.model import summarizeText
from summarizer.request.SummarizationRequest import SummarizationRequest
from summarizer.response.SummarizationResponse import SummarizationResponse

summarizer_router = APIRouter(
    prefix="/summarizer",
    tags=["Summarizer"],
    responses={404: {"description": "Not found"}}
)

@summarizer_router.post("/summarize", response_model=SummarizationResponse)
async def getSummarization(request: SummarizationRequest = Query()):
    return summarizeText(request)