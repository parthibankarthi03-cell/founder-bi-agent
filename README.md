Founder BI Agent
💼 Project Overview

Founder BI Agent is a web-based Business Intelligence (BI) platform that delivers actionable insights from Monday.com boards. Users can query metrics like revenue, deal counts, and sector performance, and receive human-readable summaries with a detailed processing trace.

Technologies used:

FastAPI – backend API

pandas – data cleaning & preprocessing

Groq LLM – natural language business summary generation

Monday.com API – live data retrieval

Workflow Diagram:


✨ Key Features

Chat-based interface for business questions

Executive-style summaries automatically generated

Trace logs show all processing steps

Handles missing/incomplete data robustly

Modular design for easy extension


📁 Project Structure
Founder-BI-Agent/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── routes/ask.py           # API endpoint for /ask
│   ├── services/
│   │   ├── llm_agent.py        # Query interpretation & LLM integration
│   │   ├── bi_engine.py        # Generates business insights
│   │   ├── data_cleaner.py     # Cleans and preprocesses data
│   │   └── monday_client.py    # Fetches data from Monday.com
│   └── config.py               # Environment configuration
├── static/
│   ├── index.html              # Frontend chat interface
│   └── images/                 # Screenshots or diagrams
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/parthibankarthi03-cell/founder-bi-agent.git
cd founder-bi-agent
2️⃣ Create a virtual environment
python -m venv venv
# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Configure environment variables

Create a .env file:

MONDAY_API_TOKEN=<your_monday_api_token>
LLM_API_KEY=<your_groq_llm_api_key>
🚀 Running the Application
uvicorn app.main:app --reload

Open browser: http://127.0.0.1:8000/

Enter questions in the chat interface

Sample Questions:

"What is the total revenue this quarter?"

"How many deals are active?"

"Provide sector-wise revenue performance."

🛠 API Endpoint
Endpoint	Method	Description
/ask	POST	Returns a business summary and trace logs

Request Example:

{
  "question": "What is the total revenue this quarter?"
}

Response Example:

{
  "answer": "Total revenue is $50,000 across 12 deals.",
  "trace": [
    {"step": "LLM Prompt Sent", "data": {...}},
    {"step": "Data Cleaned", "data": {"rows": 12}}
  ]
}
