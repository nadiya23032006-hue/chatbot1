from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Chatbot Kampus Vokasi API")

# Model request
class ChatRequest(BaseModel):
    prompt: str

# Endpoint chat
@app.post("/chat")
def chat(request: ChatRequest):
    api_key = os.environ.get("QWEN_API_KEY")  # Ambil dari environment variable
    if not api_key:
        raise HTTPException(status_code=500, detail="QWEN_API_KEY belum di-set di environment.")

    url = "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": request.prompt,
        "parameters": {"temperature": 0.3, "max_new_tokens": 200}
    }

    try:
        res = requests.post(url, headers=headers, json=data, timeout=90)
        res.raise_for_status()
        return {"reply": res.json().get("generated_text", "")}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API Error: {e}")
