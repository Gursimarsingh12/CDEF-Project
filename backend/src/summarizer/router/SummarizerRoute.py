from typing import List
from fastapi import APIRouter, Query
from summarizer.model import getSummarizations, summarizeText
from summarizer.request.SummarizationRequest import SummarizationRequest
from summarizer.response.SummarizationResponse import SummarizationResponse

summarizer_router = APIRouter(
    prefix="/summarizer",
    tags=["Summarizer"],
    responses={404: {"description": "Not found"}}
)

@summarizer_router.post("/summarize", response_model=SummarizationResponse)
async def summarize(request: SummarizationRequest = Query()):
    return await summarizeText(request)

@summarizer_router.get("/summarizations", response_model=List[SummarizationResponse])
async def get_summarizations(email: str = Query(...)):
    return await getSummarizations(email)
