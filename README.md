# DASH - Executive AI Agent Platform

![DASH Platform](./dash.png)

An AI agent for busy business leaders built on [DigitalOcean's Gradient™ AI Platform](https://www.digitalocean.com/products/gradient/platform).

DASH provides chat and Slack bot interfaces for business intelligence assistance with built-in tools for production database queries, agentic web search, and lead management.

Originally authored by [Andrew Baker](https://www.linkedin.com/in/andrewtorkbaker/) for a live demo at a DigitalOcean event in July 2025. Uses sample data adapted from [Gator](https://www.gator.works/), Andrew's SaaS business built on Slack's API.

## Features

- **Chat Interface**: [SvelteKit](https://svelte.dev/docs/kit/introduction)-based web chat with streaming responses
- **Slack Bot**: Native [Slack](https://api.slack.com/) integration with event handling
- **SQL Query Tool**: Read-only database queries for business intelligence
- **Web Search Tool**: Real-time web and news search via [Brave Search API](https://brave.com/search/api/)
- **Airtable Leads**: Create and manage qualified customer leads in [Airtable](https://www.airtable.com/guides/scale/using-airtable-api)
- **HTTP-Based Architecture**: [DigitalOcean Functions](https://www.digitalocean.com/products/functions) backend with HTTP API calls

## Architecture

The platform uses an HTTP-based architecture where:
- **DigitalOcean Functions** contain all business logic and tools
- **Chat Interface** streams responses from [FastAPI](https://fastapi.tiangolo.com/) backend
- **Slack Bot** receives events and responds via Slack API

## Prerequisites

- **Node.js 18+** - For SvelteKit frontend
- **Python 3.11+** - For FastAPI backend
- **uv** - Fast Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **doctl CLI** - [DigitalOcean command line tool](https://docs.digitalocean.com/reference/doctl/) (for function deployment)

## Quick Start

### 1. Create your DigitalOcean Gradient™ AI agent

[Create a DigitalOcean account](https://cloud.digitalocean.com/registrations/new) if you don't have one already, and then visit the "Create an agent" page: https://cloud.digitalocean.com/gen-ai/agents/new

Name your agent "DASH", and then copy + paste the agent instructions from the agent subdirectory's README: [agent/README.md](./agent/README.md#agent-instructions)

Select a model to power your agent. DASH has been tested most extensively with Llama 3.3 Instruct (70B).

Create a new workspace for your agent, and give it a name. Then click "Create Agent".

While your agent deploys, clone this repository and move on to step 2.

### 2. Create a knowledgebase for your agent (optional)

Gradient™ AI knowledge bases store and index private data sources, which your agent draws upon when generating responses for users. If you only want your DASH agent to retrieve additional context via tool calls, you can skip this step.

To create your knowledge base, [open the "Knowledge Bases" tab in the Agent Platform section of your console](https://cloud.digitalocean.com/gen-ai/knowledge-bases) and click "Create knowledge base". Name your new knowledge base "dash-kb".

Click "select data source" and choose "file upload". To use Gator's sample data (P&L statements from 2020 through 2024), upload the contents of the `agent/knowledge_base` subdirectory. Click "Add selected data source".

Choose any embeddings model and click "Create Knowledge Base".

While your knowledge base deploys and performs its initial index, proceed to step 3.

### 3. Deploy DigitalOcean Functions

DASH comes with a handful of built-in functions, which we'll connect to our DASH Agent as tools. Before we can do that, however, we need to deploy the underlying DigitalOcean Functions.

The easiest way to do that is to use the DigitalOcean CLI. [Follow these instructions to download and install doctl](https://docs.digitalocean.com/reference/doctl/).

Then, copy `agent/functions/.env.example` to `agent/functions/.env`. If you want to use the Brave and Airtable integrations, update your `.env` file to use your API keys. You can keep the `DATABASE_URL` environment variable set to `use-gator-sample-data` to use sample data drawn from Gator's production database.

Then, run these commands to deploy DASH's built-in functions to your DigitalOcean project:

```bash
cd agent/functions
doctl serverless deploy . --remote-build
```

### 4. Wire up your knowledge base and tools to your DASH agent

By now, your DASH agent, knowledge base, and functions should all be deployed. The last step before starting DASH is to connect them all together.

Return to your agent in the DigitalOcean console and open the "Resources" tab.

If you created a knowledge base in step 2, click "Add knowledge bases" and add it to your agent.

Next, scroll down to Function Routes. For each of our four built-in functions...

1. Click "Add function route"
1. Select the function from the drop down menus (like `dash/run_sql_query`)
1. Use that function's README in this repository to copy + paste the function's instructions, input, and output schemas. Choose any route name you like.
1. Click "Add function" to finish adding the function as a tool to your agent

After connecting your agent to your knowledge base and functions, you can test the connections by going to your agent's "Playground" tab. Try asking a question like "How many Slack teams have Gator installed?". The correct answer for our sample data set is 81.

Continue on to configure and run the DASH web UI and Slack interface.

### 5. Start DASH web UI

Before running the DASH web UI locally, you will need to populate the FastAPI server's `.env` file with your agent's unique endpoint URL and access key.

Copy `chat/backend/.env.example` to `chat/backend/.env`. You can find your agent's access endpoint URL from the "Agent Essentials" section of your agent's "Overview" tab. Click the "Manage Endpoint Access Keys" link to create a new access key to use in your `.env` file.

Next, install and run the backend and frontend servers. You can either install the dependencies yourself or use DASH's docker compose configuration:

**To start DASH using Docker**

```bash
cd chat
docker compose up
```

DASH should then be running at http://localhost:5173 or a similar port.

**To install DASH's dependencies without Docker**

```bash
# Install frontend dependencies
cd chat
npm install

# Start the frontend
npm run dev

# Backend (in separate terminal)
cd chat/backend
uv sync

# Copy and populate the environment variables using your Agent's endpoint and access key
cp .env.example .env

# Start the backend
uv run python main.py
```

DASH should then be running at http://localhost:5173 or a similar port.

Congrats! You have now successfully configured DASH 🏃‍♂️

### 6. Slack integration (optional)

DASH can also join your team as a Slack bot. See the instructions in [chat/backend/README_SLACK.md](./chat/backend/README_SLACK.md) for more details.

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

## Environment Variables

Each component requires specific environment variables:

### DigitalOcean Functions (`agent/functions/project.yml`)
```yaml
DATABASE_URL: "${DATABASE_URL}"  # Or use-gator-sample-data for testing
BRAVE_API_KEY: "${BRAVE_API_KEY}"
AIRTABLE_ACCESS_TOKEN: "${AIRTABLE_ACCESS_TOKEN}"
AIRTABLE_BASE_ID: "${AIRTABLE_BASE_ID}"
AIRTABLE_TABLE_ID: "${AIRTABLE_TABLE_ID}"
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
