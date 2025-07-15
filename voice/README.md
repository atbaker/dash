# DASH Voice Assistant

A voice-based AI assistant powered by Pipecat for real-time conversations with business intelligence capabilities.

## Features

- **WebRTC Voice Streaming**: Real-time voice conversations
- **HTTP-Based Tools**: Calls DigitalOcean Functions for all business logic
- **Business Intelligence**: SQL queries, web search, and lead management
- **Pipecat Pipeline**: Advanced voice processing with OpenAI integration

## Architecture

The voice assistant uses an HTTP-based architecture:
- **Pipecat Framework**: Handles voice pipeline, STT, TTS, and LLM integration
- **HTTP Wrappers**: Lightweight functions that call DigitalOcean Functions
- **DigitalOcean Functions**: Backend services containing all business logic

## Quick Start

### Prerequisites
- Python 3.11+
- uv (Python package manager)
- DigitalOcean Functions deployed
- API keys for Deepgram, Cartesia, and DigitalOcean

### Setup

```bash
# Install dependencies
uv sync

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys and DO Functions URL

# Start voice assistant
uv run python main.py
```

## Environment Variables

Create a `.env` file with:

```env
# Voice Services
DEEPGRAM_API_KEY=your_deepgram_key
CARTESIA_API_KEY=your_cartesia_key
CARTESIA_VOICE_ID=your_voice_id

# DigitalOcean
DO_MODEL_ACCESS_KEY=your_do_model_key
DO_FUNCTIONS_BASE_URL=https://faas-xxx.doserverless.co/api/v1/web/fn-xxx/gator
```

## HTTP Tools

The voice assistant includes these HTTP wrapper functions:

### run_sql_query.py
```python
async def run_sql_query(params: FunctionCallParams):
    # HTTP call to DigitalOcean Function
    response = requests.post(f"{base_url}/run_sql_query", 
                           json={"query": query}, timeout=30)
```

### web_search.py
```python
async def web_search(params: FunctionCallParams):
    # HTTP call to DigitalOcean Function
    response = requests.post(f"{base_url}/web_search", 
                           json={"query": query}, timeout=30)
```

### airtable_leads.py
```python
async def airtable_leads(params: FunctionCallParams):
    # HTTP call to DigitalOcean Function
    response = requests.post(f"{base_url}/airtable_leads", 
                           json={"customer": customer, "website": website, "notes": notes}, 
                           timeout=30)
```

## How It Works

1. **Voice Input**: User speaks into microphone
2. **Speech-to-Text**: Deepgram converts speech to text
3. **LLM Processing**: OpenAI processes text and determines tool usage
4. **Tool Execution**: HTTP calls to DigitalOcean Functions
5. **Response Generation**: LLM generates response based on tool results
6. **Text-to-Speech**: Cartesia converts response to speech
7. **Voice Output**: User hears AI response

## Deployment

The voice assistant is designed to run as a service with persistent WebRTC connections:

```bash
# Production deployment
uv run python main.py
```

## Dependencies

- **pipecat-ai**: Voice conversation pipeline
- **requests**: HTTP client for DigitalOcean Functions
- **python-dotenv**: Environment variable management
- **loguru**: Enhanced logging