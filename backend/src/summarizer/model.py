from typing import List
from transformers import pipeline
from fastapi import HTTPException
from summarizer.request.SummarizationRequest import SummarizationRequest
from summarizer.response.SummarizationResponse import SummarizationResponse
from auth.DatabaseController import getSummarizationCollection
from datetime import datetime

try:
    summarizer = pipeline("summarization", model="google-t5/t5-small")
except Exception as e:
    raise RuntimeError("Failed to load the summarization model.") from e

async def summarizeText(request: SummarizationRequest) -> SummarizationResponse:
    if len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        summary = summarizer(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length,
            do_sample=False,
        )[0]["summary_text"]
        document = {
            "email": request.email,
            "text": request.text,
            "summary": summary,
            "uploaded_at": datetime.now()
        }
        summarization_collection = await getSummarizationCollection()
        summarization_collection.insert_one(document)
        return SummarizationResponse(
            email=request.email,
            text=request.text,
            summary=summary,
            uploaded_at=document["uploaded_at"].strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


async def getSummarizations(email: str) -> List[SummarizationResponse]:
    summarization_collection = await getSummarizationCollection()
    documents = summarization_collection.find({"email": email})
    return [SummarizationResponse(**document) async for document in documents]