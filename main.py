from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from backend.utils.intent import classifyIntent
from backend.utils.query import sendQuery
from backend.utils.memory import getHistory, addHistory
from backend.utils.collection import createCollection
from backend.utils.chunker import chunkFiles

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://next-chatbot-git-main-nobel-suhendras-projects.vercel.app"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize collection
chunks = chunkFiles()
collection = createCollection(chunks)

class Message(BaseModel):
    text: str
    isUser: bool

class ChatRequest(BaseModel):
    message: str
    userId: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Store user message in history
        addHistory(request.userId, "user", request.message)
        
        # Classify intent
        intent = classifyIntent(request.message)
        
        if intent == "vector":
            # Get answer from vector search
            response = sendQuery(request.message, collection)
        else:
            # For general queries, you might want to use a different model or response
            response = "I'm a general assistant. How can I help you?"
        
        # Store bot response in history
        addHistory(request.userId, "assistant", response)
        
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{user_id}")
async def get_chat_history(user_id: str):
    try:
        history = getHistory(user_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
