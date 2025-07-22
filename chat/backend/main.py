"""
Simplified FastAPI backend for DASH chat interface.
Provides JSON streaming endpoints for Svelte frontend.
"""
import os
import json
import asyncio
import hashlib
import hmac
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from slack_bot import SlackBot
from chat_service import stream_chat_response

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
    
    # Slack configuration
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")
    
    def validate(self) -> None:
        """Validate that required settings are present."""
        if not self.DO_AGENT_ENDPOINT:
            raise ValueError("DO_AGENT_ENDPOINT environment variable is required")
        if not self.DO_AGENT_ACCESS_KEY:
            raise ValueError("DO_AGENT_ACCESS_KEY environment variable is required")
    
    def validate_slack(self) -> None:
        """Validate Slack configuration."""
        if not self.SLACK_BOT_TOKEN:
            raise ValueError("SLACK_BOT_TOKEN environment variable is required for Slack integration")
        if not self.SLACK_SIGNING_SECRET:
            raise ValueError("SLACK_SIGNING_SECRET environment variable is required for Slack integration")

config = Config()

# Validate configuration on startup
try:
    config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    if not config.DEBUG:
        raise

# Slack bot will be initialized after function definitions
slack_bot = None

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
    # Ensure endpoint has proper format - OpenAI client will append /chat/completions
    base_url = config.DO_AGENT_ENDPOINT
    if base_url.endswith('/api/v1/chat/completions'):
        # Remove the path since OpenAI client adds it automatically
        base_url = base_url.replace('/api/v1/chat/completions', '')
    elif not base_url.endswith('/api/v1'):
        # Add /api/v1 if not present
        base_url = base_url.rstrip('/') + '/api/v1'
    
    return OpenAI(
        base_url=base_url,
        api_key=config.DO_AGENT_ACCESS_KEY,
    )

# Initialize Slack bot if configuration is available
if config.SLACK_BOT_TOKEN and config.SLACK_SIGNING_SECRET:
    try:
        config.validate_slack()
        client = get_openai_client()
        slack_bot = SlackBot(config.SLACK_BOT_TOKEN, client)
        print("Slack bot initialized successfully")
    except ValueError as e:
        print(f"Slack configuration error: {e}")
        if not config.DEBUG:
            slack_bot = None
else:
    print("Slack integration disabled (missing SLACK_BOT_TOKEN or SLACK_SIGNING_SECRET)")

async def stream_openai_response_json(message: str, history: list[dict]) -> AsyncGenerator[str, None]:
    """Stream response from DigitalOcean Agent as JSON lines (for web interface)."""
    try:
        client = get_openai_client()
        
        # Stream chunks as JSON using shared service
        async for content in stream_chat_response(client, message, history):
            yield json.dumps({"content": content}) + "\n"
            
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
        stream_openai_response_json(chat_request.message, chat_request.history),
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

def verify_slack_signature(request_body: bytes, timestamp: str, signature: str) -> bool:
    """Verify Slack request signature."""
    if not config.SLACK_SIGNING_SECRET:
        return False
    
    # Create signature base string
    sig_basestring = f"v0:{timestamp}:{request_body.decode('utf-8')}"
    
    # Create expected signature
    expected_signature = 'v0=' + hmac.new(
        config.SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack event subscriptions."""
    if not slack_bot:
        raise HTTPException(status_code=501, detail="Slack integration not configured")
    
    # Get request body and headers
    body = await request.body()
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    
    # Verify signature
    if not verify_slack_signature(body, timestamp, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    try:
        event_data = json.loads(body.decode('utf-8'))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Handle URL verification challenge
    if event_data.get("type") == "url_verification":
        return {"challenge": event_data.get("challenge")}
    
    # Handle events
    if event_data.get("type") == "event_callback":
        # Process event in background to respond quickly to Slack
        asyncio.create_task(slack_bot.handle_slack_event(event_data))
        return {"status": "ok"}
    
    return {"status": "ignored"}

@app.get("/")
async def root():
    """Root endpoint."""
    endpoints = {
        "chat": "/api/chat/stream",
        "health": "/health"
    }
    
    if slack_bot:
        endpoints["slack_events"] = "/slack/events"
    
    return {
        "message": "DASH Chat Backend",
        "version": "0.1.0",
        "endpoints": endpoints,
        "slack_enabled": slack_bot is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )