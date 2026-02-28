# bi_engine.py

import json
from groq import Groq
from app.config import LLM_API_KEY

# Initialize Groq client
client = Groq(api_key=LLM_API_KEY)

BOARD_MAP = {
    "deals": 123456789,        # replace with your Deals board ID
    "work_orders": 987654321   # replace with your Work Orders board ID
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
        model="llama-3.3-70b-versatile",
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
        parsed_llm = {
            "board": "deals",
            "metric": "count",
            "filters": {"sector": None, "quarter": None}
        }

    board_type = parsed_llm["board"]
    parsed = {
        "board_id": BOARD_MAP.get(board_type, None),
        "board_type": board_type,
        "metric": parsed_llm["metric"],
        "filters": parsed_llm["filters"],
        "original_question": question
    }

    trace.add("LLM Parsed Output", parsed)
    return parsed

def generate_insight(cleaned_data, parsed_query, trace):
    trace.add("Generating Insight", {})

    # Check columns safely
    total_revenue = cleaned_data['revenue'].sum() if 'revenue' in cleaned_data.columns else 0
    total_deals = len(cleaned_data)

    sector_summary = None
    if parsed_query.get("metric") == "sector_analysis" and 'sector' in cleaned_data.columns:
        sector_summary = cleaned_data.groupby("sector")['revenue'].sum().to_dict() \
            if 'revenue' in cleaned_data.columns else {}

    summary_prompt = f"""
You are a business analyst AI.

Metrics:
- Total Revenue: {total_revenue}
- Total Deals: {total_deals}
"""

    if sector_summary:
        summary_prompt += f"- Sector Performance: {sector_summary}\n"

    summary_prompt += "\nExplain this in a clear, concise business summary suitable for executives."

    trace.add("Summary Prompt Created", {"prompt": summary_prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a business intelligence summarizer."},
            {"role": "user", "content": summary_prompt}
        ],
        temperature=0.3
    )

    business_summary = response.choices[0].message.content
    trace.add("Business Summary Generated", {"summary": business_summary})

    return business_summary