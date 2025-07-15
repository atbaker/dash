"""
Simplified FastAPI backend for DASH chat interface.
Provides JSON streaming endpoints for Svelte frontend.
"""
import os
import json
import asyncio
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatMessage(BaseModel):
    message: str

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []  # Previous conversation messages

class Config:
    """Configuration loaded from environment variables."""
    DO_AGENT_ENDPOINT: str = os.getenv("DO_AGENT_ENDPOINT", "")
    DO_AGENT_ACCESS_KEY: str = os.getenv("DO_AGENT_ACCESS_KEY", "")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    def validate(self) -> None:
        """Validate that required settings are present."""
        if not self.DO_AGENT_ENDPOINT:
            raise ValueError("DO_AGENT_ENDPOINT environment variable is required")
        if not self.DO_AGENT_ACCESS_KEY:
            raise ValueError("DO_AGENT_ACCESS_KEY environment variable is required")

config = Config()

# Validate configuration on startup
try:
    config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    if not config.DEBUG:
        raise

# Create FastAPI app
app = FastAPI(
    title="DASH Chat Backend",
    description="Simplified JSON API for DASH chat interface",
    version="0.1.0"
)

# Configure CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173", "*"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_openai_client() -> OpenAI:
    """Create OpenAI client configured for DigitalOcean Agent endpoint."""
    return OpenAI(
        base_url=config.DO_AGENT_ENDPOINT,
        api_key=config.DO_AGENT_ACCESS_KEY,
    )

async def stream_openai_response(message: str, history: list[dict]) -> AsyncGenerator[str, None]:
    """Stream response from DigitalOcean Agent."""
    try:
        client = get_openai_client()
        
        # Build full conversation messages including history
        messages = []
        
        # Add conversation history (alternating user/assistant messages)
        messages.extend(history)
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        # Create streaming request
        stream = client.chat.completions.create(
            model="n/a",  # Model is configured in DO Agent
            messages=messages,
            stream=True,
            extra_body={"include_retrieval_info": True}
        )
        
        # Stream chunks as JSON
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield json.dumps({"content": content}) + "\n"
                # Small delay to ensure chunk is sent
                await asyncio.sleep(0.01)
        
        # Send completion signal
        yield json.dumps({"complete": True}) + "\n"
        
    except Exception as e:
        # Send error
        yield json.dumps({"error": str(e)}) + "\n"

@app.post("/api/chat/stream")
async def chat_stream(chat_request: ChatRequest):
    """Stream chat response as JSON lines."""
    
    if not chat_request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    return StreamingResponse(
        stream_openai_response(chat_request.message, chat_request.history),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
            "Transfer-Encoding": "chunked",
        }
    )

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "config": {"has_endpoint": bool(config.DO_AGENT_ENDPOINT)}}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "DASH Chat Backend",
        "version": "0.1.0",
        "endpoints": {
            "chat": "/api/chat/stream",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )