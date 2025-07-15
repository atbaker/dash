# DASH - Executive AI Agent Platform

An Executive AI agent platform built on DigitalOcean's GenAI Platform. DASH provides multiple interfaces for business intelligence assistance with access to production database queries, web search capabilities, and Airtable lead management.

## Features

- **Chat Interface**: SvelteKit-based web chat with streaming responses
- **Voice Assistant**: Pipecat-powered voice conversations with WebRTC
- **SQL Query Tool**: Read-only database queries for business intelligence
- **Web Search Tool**: Real-time web and news search via Brave Search API
- **Airtable Leads**: Create and manage qualified customer leads
- **HTTP-Based Architecture**: DigitalOcean Functions backend with HTTP API calls

## Architecture

The platform uses an HTTP-based architecture where:
- **DigitalOcean Functions** contain all business logic and tools
- **Voice Agent** makes HTTP calls to DigitalOcean Functions
- **Chat Interface** streams responses from FastAPI backend
- **Self-contained Functions** each contain their own business logic

## Quick Start

### 1. Deploy DigitalOcean Functions
```bash
cd agent/functions
# Set up environment variables in project.yml
doctl serverless deploy . --remote-build
```

### 2. Start Chat Interface
```bash
# Frontend
cd chat
npm install
npm run dev

# Backend (in separate terminal)
cd chat/backend
uv sync
uv run python main.py
```

### 3. Start Voice Assistant
```bash
cd voice
uv sync
# Set up .env file with API keys and DO Functions URL
uv run python main.py
```

## Project Structure

```
dash/
├── agent/                    # DigitalOcean Functions
│   └── functions/
│       └── packages/gator/
│           ├── run_sql_query/     # Database query function
│           ├── web_search/        # Web search function
│           └── airtable_leads/    # Airtable lead creation
├── chat/                     # SvelteKit chat interface
│   ├── backend/             # FastAPI backend
│   └── src/                 # Svelte frontend
├── voice/                   # Pipecat voice assistant
│   ├── functions/           # HTTP wrappers for DO Functions
│   └── main.py             # Voice pipeline
└── README.md               # This file
```

## Tools Available

- **run_sql_query**: Query production database for business metrics
- **web_search**: Search the web for current information and market research
- **airtable_leads**: Create qualified lead records in Airtable database

## Environment Variables

Each component requires specific environment variables:

### DigitalOcean Functions (`agent/functions/project.yml`)
```yaml
DATABASE_URL: "${DATABASE_URL}"
BRAVE_API_KEY: "${BRAVE_API_KEY}"
AIRTABLE_ACCESS_TOKEN: "${AIRTABLE_ACCESS_TOKEN}"
AIRTABLE_BASE_ID: "${AIRTABLE_BASE_ID}"
AIRTABLE_TABLE_ID: "${AIRTABLE_TABLE_ID}"
```

### Chat Backend (`chat/backend/.env`)
```env
DO_AGENT_ENDPOINT=https://your-agent-endpoint
DO_AGENT_ACCESS_KEY=your-access-key
```

### Voice Assistant (`voice/.env`)
```env
DEEPGRAM_API_KEY=your_deepgram_key
CARTESIA_API_KEY=your_cartesia_key
CARTESIA_VOICE_ID=your_voice_id
DO_MODEL_ACCESS_KEY=your_do_model_key
DO_FUNCTIONS_BASE_URL=https://faas-xxx.doserverless.co/api/v1/web/fn-xxx/gator
```
