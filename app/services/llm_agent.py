from groq import Groq
from app.config import LLM_API_KEY
import json

client = Groq(api_key=LLM_API_KEY)
import os
print("GROQ KEY:", os.getenv("GROQ_API_KEY"))

BOARD_MAP = {
    "deals": 123456789,        # replace with your Deals board ID
    "work_orders": 987654321   # replace with your Works board ID
}

def interpret_query(question, trace):

    prompt = f"""
You are a strict Business Intelligence Agent.

User Question:
{question}

Rules:
- If question contains "revenue", "sales", "income", return metric = "revenue"
- If question contains "how many", "number of", return metric = "count"
- If question contains "sector", return metric = "sector_analysis"

Return ONLY valid JSON.

Format:
{{
  "board": "deals or work_orders",
  "metric": "count or revenue or sector_analysis",
  "filters": {{
      "sector": null,
      "quarter": null
  }}
}}
"""

    trace.add("LLM Prompt Sent", {"prompt": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # 🔥 Model name goes here
        messages=[
            {"role": "system", "content": "You are a structured JSON generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        parsed_llm = json.loads(content)
    except:
        # fallback if LLM outputs invalid JSON
        parsed_llm = {
            "board": "deals",
            "metric": "count",
            "filters": {"sector": None, "quarter": None}
        }

    board_type = parsed_llm["board"]

    parsed = {
        "board_id": BOARD_MAP[board_type],
        "board_type": board_type,
        "metric": parsed_llm["metric"],
        "filters": parsed_llm["filters"],
        "original_question": question
    }

    trace.add("LLM Parsed Output", parsed)

    return parsed