from transformers import pipeline
from fastapi import HTTPException
from summarizer.request.SummarizationRequest import SummarizationRequest
from summarizer.response.SummarizationResponse import SummarizationResponse

try:
    summarizer = pipeline("summarization", model="google-t5/t5-small")
except Exception as e:
    raise RuntimeError("Failed to load the summarization model.") from e

def summarizeText(request: SummarizationRequest) -> SummarizationResponse:
    if len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    try:
        summary = summarizer(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length,
            do_sample=False,
        )
        return SummarizationResponse(summary=summary[0]["summary_text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")