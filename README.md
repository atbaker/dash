# DASH - Executive AI Agent Platform

![DASH Platform](./dash.png)

An Executive AI agent platform built on DigitalOcean's GenAI Platform. DASH provides chat and Slack bot interfaces for business intelligence assistance with access to production database queries, web search capabilities, and Airtable lead management.

## Features

- **Chat Interface**: SvelteKit-based web chat with streaming responses
- **Slack Bot**: Native Slack integration with event handling
- **SQL Query Tool**: Read-only database queries for business intelligence
- **Web Search Tool**: Real-time web and news search via Brave Search API
- **Airtable Leads**: Create and manage qualified customer leads
- **HTTP-Based Architecture**: DigitalOcean Functions backend with HTTP API calls

## Architecture

The platform uses an HTTP-based architecture where:
- **DigitalOcean Functions** contain all business logic and tools
- **Chat Interface** streams responses from FastAPI backend
- **Slack Bot** receives events and responds via Slack API
- **Self-contained Functions** each contain their own business logic

## Prerequisites

- **Node.js 18+** - For SvelteKit frontend
- **Python 3.11+** - For FastAPI backend
- **uv** - Fast Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **doctl CLI** - DigitalOcean command line tool (for function deployment)

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
# Copy environment variables
cp .env.example .env
# Edit .env with your DigitalOcean Agent credentials
uv run python main.py
```

### 3. Optional: Setup Slack Bot
For Slack integration, see detailed setup instructions in [chat/backend/README_SLACK.md](chat/backend/README_SLACK.md).


## Project Structure

```
dash/
├── agent/                    # DigitalOcean Functions
│   ├── functions/
│   │   └── packages/gator/
│   │       ├── run_sql_query/     # Database query function
│   │       ├── web_search/        # Web search function
│   │       ├── airtable_leads/    # Airtable lead creation
│   │       ├── list_airtable_leads/ # List leads from Airtable
│   │       └── get_latest_workspaces/ # Get recent workspace installs
│   └── knowledge_base/       # Sample P&L data and other documents
├── chat/                     # SvelteKit chat interface + Slack bot
│   ├── backend/             # FastAPI backend with Slack integration
│   └── src/                 # Svelte frontend
├── scripts/                  # Database migration and setup scripts
└── README.md               # This file
```

## Tools Available

- **run_sql_query**: Query production database for business metrics (includes SQLite sample data mode)
- **web_search**: Search the web for current information and market research
- **add_airtable_lead**: Create qualified lead records in Airtable database
- **list_airtable_leads**: Retrieve recent leads from Airtable for pipeline review
- **get_latest_workspaces**: Get recent workspace installations (demo-optimized)

## Environment Variables

Each component requires specific environment variables:

### DigitalOcean Functions (`agent/functions/project.yml`)
```yaml
DATABASE_URL: "${DATABASE_URL}"  # Or use-gator-sample-data for testing
BRAVE_API_KEY: "${BRAVE_API_KEY}"
AIRTABLE_ACCESS_TOKEN: "${AIRTABLE_ACCESS_TOKEN}"
AIRTABLE_BASE_ID: "${AIRTABLE_BASE_ID}"
AIRTABLE_TABLE_ID: "${AIRTABLE_TABLE_ID}"
DO_FUNCTIONS_BASE_URL: "${DO_FUNCTIONS_BASE_URL}"  # For get_latest_workspaces function
```

### Chat Backend (`chat/backend/.env`)
```env
DO_AGENT_ENDPOINT=https://your-agent-endpoint
DO_AGENT_ACCESS_KEY=your-access-key
DEBUG=true

# Optional: For Slack integration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
```

### Chat Frontend (`chat/.env`)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Sample Data Mode

For testing without a production database, the system includes sample data:

- Set `DATABASE_URL=use-gator-sample-data` in `agent/functions/.env`
- Sample SQLite database (`gator_sample.db`) contains anonymized workspace and user data
- Sample P&L data available in `agent/knowledge_base/` directory

## Troubleshooting

### Common Issues
1. **Functions not deploying**: Ensure all environment variables are set in `project.yml`
2. **Chat interface not loading**: Check that backend is running on port 8000
3. **Database connection errors**: Verify `DATABASE_URL` format or use sample data mode
4. **Slack bot not responding**: Check webhook URL and verify signing secret
5. **Build failures**: Run `npm run check` for TypeScript errors

### Getting Help
- Check individual component README files for detailed setup
- Review `.env.example` files for required environment variables
- Enable `DEBUG=true` in backend for verbose logging
