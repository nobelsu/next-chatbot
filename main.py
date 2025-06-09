from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from backend.utils.intent import classifyIntent
from backend.utils.rewrite import rewriteQuery
from backend.utils.query import sendQuery
from backend.utils.memory import getHistory, addHistory
from backend.utils.collection import createCollection
from backend.utils.chunker import chunkFiles
from backend.utils.sql import querySQL

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
chunks, tableCnt = chunkFiles()
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
        addHistory(request.userId, "user", request.message)
        
        q = rewriteQuery(request.message)
        intent = classifyIntent(q)
        
        if intent == "vector":
            response = sendQuery(q, collection)
        elif intent == "general":
            response = "I'm a general assistant. How can I help you?"
        else:
            response = querySQL(q, tableCnt)
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
