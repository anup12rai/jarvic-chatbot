
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from groq import Groq

from instruction import SYSTEM_INSTRUCTION

load_dotenv()

app = FastAPI(
    title="JARVIC CHATBOT API",
    version="1.0.0"
)

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing")

client = Groq(api_key=api_key)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[dict] = Field(default_factory=list)


@app.get("/")
def home():
    return {
        "success": True,
        "app": "JARVIC CHATBOT",
        "status": "online"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_INSTRUCTION
            }
        ]

       
        for item in request.history[-10:]:
            role = item.get("role")
            content = item.get("content")

            if role in ("user", "assistant") and isinstance(content, str):
                messages.append({
                    "role": role,
                    "content": content[:4000]
                })

    
        messages.append({
            "role": "user",
            "content": request.message
        })

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_completion_tokens=500
        )

        answer = response.choices[0].message.content

        return {
            "success": True,
            "assistant": "JARVIC",
            "response": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
