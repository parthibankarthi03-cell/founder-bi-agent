Project Structure
your_project/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── routes/ask.py           # API endpoint for /ask
│   ├── services/
│   │   ├── llm_agent.py        # Query interpretation and LLM calls
│   │   ├── bi_engine.py        # Generate business insights
│   │   ├── data_cleaner.py     # Clean and preprocess data
│   │   └── monday_client.py    # Fetch data from Monday.com
│   └── config.py               # API keys and configuration
├── static/
│   └── index.html              # Frontend chat interface
├── requirements.txt            # Python dependencies
└── README.md                   # This file