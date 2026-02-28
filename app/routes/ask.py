# app/routes/ask.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import pandas as pd

# Import your existing services
from app.services.llm_agent import interpret_query
from app.services.monday_client import fetch_board_data
from app.services.data_cleaner import clean_data
from app.services.bi_engine import generate_insight

router = APIRouter()

# ---------------------------
# Pydantic Schemas
# ---------------------------
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    trace: List[Dict[str, Any]] = []

# ---------------------------
# Simple Trace Logger
# ---------------------------
class TraceLogger:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def add(self, step: str, data: Any):
        self.logs.append({"step": step, "data": data})
        print(f"[TRACE] {step}: {data}")

    def get_trace(self):
        return self.logs

# ---------------------------
# Ask Endpoint
# ---------------------------
@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    trace = TraceLogger()

    try:
        # Validate input
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty.")

        # Step 1: Interpret Query
        parsed_query = interpret_query(request.question, trace)
        if not parsed_query:
            raise HTTPException(status_code=500, detail="Failed to interpret query.")

        # Step 2: Fetch Live Data from Monday
        raw_data = fetch_board_data(parsed_query, trace)
        if raw_data is None or len(raw_data) == 0:
            raise HTTPException(status_code=500, detail="Failed to fetch data from Monday.")

        # Step 3: Clean Data
        cleaned_data = clean_data(raw_data, trace)
        if cleaned_data is None or cleaned_data.empty:
            raise HTTPException(status_code=500, detail="Data cleaning failed.")

        # Step 4: Generate Insight
        answer = generate_insight(cleaned_data, parsed_query, trace)
        if not answer:
            raise HTTPException(status_code=500, detail="Insight generation failed.")

        # Return Response
        return QueryResponse(answer=answer, trace=trace.get_trace())

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")