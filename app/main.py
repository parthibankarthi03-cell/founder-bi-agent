from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ask import router as ask_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


app = FastAPI(title="Monday BI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_router)
from app.config import MONDAY_API_TOKEN, LLM_API_KEY

print("Monday token loaded:", MONDAY_API_TOKEN is not None)
print("Groq key loaded:", LLM_API_KEY is not None)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")