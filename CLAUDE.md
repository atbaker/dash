# CLAUDE.md - DASH Project Guide

## Project Overview

DASH is an Executive AI agent platform built on DigitalOcean's GenAI Platform. It provides multiple interfaces for business intelligence assistance with access to production database queries, web search capabilities, and Airtable lead management. The project consists of three main components: chat interface, Slack bot, and serverless functions.

## Project Structure

```
dash/
├── chat/                      # SvelteKit chat interface + Slack bot
│   ├── backend/              # FastAPI backend for chat + Slack
│   ├── src/                  # Svelte frontend components
│   │   ├── lib/
│   │   │   ├── components/   # Svelte components
│   │   │   ├── stores/       # State management
│   │   │   └── api/          # API communication
│   │   └── routes/           # SvelteKit routes
│   ├── package.json          # Node.js dependencies
│   ├── svelte.config.js      # SvelteKit configuration
│   ├── vite.config.ts        # Vite build configuration
│   └── tailwind.config.js    # Tailwind CSS configuration
└── agent/                    # DigitalOcean Functions
    ├── functions/
    │   ├── project.yml      # Function deployment config
    │   └── packages/gator/  # Self-contained function implementations
    │       ├── run_sql_query/    # SQL query DO Function
    │       │   ├── __main__.py   # Function entry point
    │       │   ├── db_utils.py   # Database utilities
    │       │   ├── sql_utils.py  # SQL validation
    │       │   └── gator_sample.db # Sample SQLite database
    │       ├── web_search/       # Web search DO Function
    │       │   ├── __main__.py   # Function entry point
    │       │   └── web_search.py # Web search logic
    │       ├── add_airtable_lead/ # Create Airtable leads
    │       │   ├── __main__.py   # Function entry point
    │       │   └── add_airtable_lead.py # Airtable logic
    │       ├── list_airtable_leads/ # List Airtable leads
    │       └── get_latest_workspaces/ # Get recent workspaces
    └── knowledge_base/       # Sample data and documents
        ├── sample_pnl_2020.csv  # Sample P&L data
        ├── sample_pnl_2021.csv
        ├── sample_pnl_2022.csv
        ├── sample_pnl_2023.csv
        └── sample_pnl_2024.csv
```

## Technologies Used

### Frontend (Chat Interface)
- **SvelteKit 2.0** with **Svelte 5** - Modern reactive framework
- **TypeScript** - Type safety and better DX
- **Tailwind CSS 4.0** - Utility-first styling
- **Vite** - Build tool with HMR
- **Flowbite Svelte** - UI component library
- **Marked** + **DOMPurify** - Markdown rendering with sanitization

### Backend Services
- **FastAPI** - Modern Python web framework for chat backend and Slack bot
- **Slack SDK** - Slack API integration for bot functionality
- **OpenAI SDK** - LLM integration via DigitalOcean GenAI Platform
- **PostgreSQL** (psycopg3) - Database connectivity
- **Uvicorn** - ASGI server

### Infrastructure
- **DigitalOcean App Platform** - Static site hosting
- **DigitalOcean Functions** - Serverless function execution
- **DigitalOcean GenAI Platform** - AI agent orchestration

### Development Tools
- **uv** - Fast Python package management
- **Loguru** - Enhanced Python logging
- **python-dotenv** - Environment variable management

## Key Architecture Patterns

### 1. HTTP-Based Tool Architecture
Tools are implemented as self-contained DigitalOcean Functions and called via HTTP by the chat and Slack interfaces. This eliminates code duplication and cross-platform build issues:

**DigitalOcean Functions (`/agent/functions/packages/gator/*/`)**: Self-contained implementations with all business logic
**Chat/Slack Integration**: Both interfaces make HTTP calls to the same DigitalOcean Functions

Example implementation pattern:
```python
# /agent/functions/packages/gator/tool_name/__main__.py - DO Function
from tool_name import core_function

def main(event, context):
    # Self-contained tool implementation
    result = core_function(event.get('param1'), event.get('param2'))
    return {'statusCode': 200, 'body': result}

# Chat/Slack interfaces call the same DO Functions via HTTP
# This ensures consistency across all interfaces
```

### 2. Reactive State Management
Chat interface uses Svelte stores for clean, reactive state updates:
```typescript
// Add message and start streaming
chatStore.addUserMessage(message);
const streamingId = chatStore.startAssistantMessage();
chatStore.appendStreamingContent(chunk);
chatStore.completeStreaming();
```

### 3. Streaming JSON Architecture
Chat backend streams responses as JSON lines rather than SSE:
```json
{"content": "Hello"}
{"content": " there!"}
{"complete": true}
```

### 4. Function Registration Pattern
Both chat and Slack interfaces use the same DigitalOcean Functions:
- `run_sql_query` - Database queries for business intelligence (supports sample data mode)
- `web_search` - External information and current events
- `add_airtable_lead` - Create qualified lead records in Airtable
- `list_airtable_leads` - Retrieve recent leads from Airtable
- `get_latest_workspaces` - Get recent workspace installations (demo-optimized)

### 5. Component-Based UI
Modular Svelte components with clear separation:
- `ChatMessage.svelte` - Individual message display
- `MessageList.svelte` - Scrolling container
- `ChatInput.svelte` - User input with validation
- `ThemeToggle.svelte` - Dark/light mode

## Available Scripts

### Chat Interface
```bash
# Frontend development
npm run dev          # Start dev server (http://localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build
npm run check        # TypeScript type checking
npm run check:watch  # Watch mode type checking

# Backend development
cd backend
uv sync             # Install dependencies
uv run python main.py  # Start FastAPI server (http://localhost:8000)
```


### DigitalOcean Functions
```bash
cd agent/functions
doctl serverless deploy . --remote-build
```

## Environment Variables

### Chat Backend (`chat/backend/.env`)
```env
DO_AGENT_ENDPOINT=https://your-agent-endpoint
DO_AGENT_ACCESS_KEY=your-access-key
DEBUG=true
```

### Chat Frontend (`chat/.env`)
```env
VITE_API_BASE_URL=http://localhost:8000
```


### Functions (`agent/functions/.env`)
```env
# Database: Use production PostgreSQL or sample data mode
DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require
# DATABASE_URL=use-gator-sample-data  # For testing with SQLite sample data

# External APIs
BRAVE_API_KEY=your_brave_api_key
AIRTABLE_ACCESS_TOKEN=your_airtable_token
AIRTABLE_BASE_ID=your_airtable_base_id
AIRTABLE_TABLE_ID=your_airtable_table_id

# Function communication
DO_FUNCTIONS_BASE_URL=https://faas-xxx.doserverless.co/api/v1/web/fn-xxx/gator
```

## AI Agent Capabilities

The DASH AI assistant can help with:

## Sample Data Mode

For development and testing, DASH includes sample data that works without external dependencies:

- **Sample Database**: When `DATABASE_URL=use-gator-sample-data` is set, functions use an anonymized SQLite database (`gator_sample.db`) with realistic workspace and user data
- **Sample P&L Data**: The knowledge base includes 5 years of sample Profit & Loss statements (2020-2024) showing realistic SaaS business growth patterns
- **Demo Workspaces**: Sample data includes 82 fictional companies with realistic names and domains for demonstration purposes

This allows developers to:
- Test all functionality without setting up a production database
- Demonstrate capabilities using realistic but anonymized data
- Develop and debug locally without external API dependencies

## AI Assistant Capabilities

With sample or production data, the DASH AI assistant can help with:

### Business Intelligence
- **Revenue metrics** and financial performance
- **Customer usage patterns** and engagement analysis
- **User growth** and retention tracking
- **Feature adoption** and product analytics
- **Business KPIs** and trend analysis

### External Context
- **Market research** and competitor analysis
- **Industry trends** and news
- **Current events** affecting business

### Lead Management
- **Airtable integration** for creating qualified lead records
- **Three-step workflow**: query recent installs → research companies → create lead entries
- **Sales follow-up tracking** with customer names, websites, and LLM-authored insights

### Technical Implementation
- **SQL queries** limited to SELECT/WITH statements only
- **Results truncated** to 1000 rows for safety
- **30-second timeout** on database queries
- **Web search** via Brave Search API
- **Airtable lead creation** with Personal Access Token authentication

## Development Guidelines

### Code Organization
1. **Self-contained functions** each package contains all required business logic
2. **Component-specific logic** stays within respective directories
3. **Environment variables** are validated on startup
4. **Error handling** is consistent across all interfaces

### Tool Implementation Guidelines
When implementing new tools, follow the consistent architecture pattern:

1. **DigitalOcean Functions**: Create self-contained function in `/agent/functions/packages/gator/tool_name/`
   - Implement all business logic within the function package
   - Create `__main__.py` for the function entry point
   - Include all required utilities (e.g., `tool_name.py`, `utils.py`)
   - Handle DO Functions event/context pattern
   - Return proper HTTP status codes and response format
   - Include appropriate error handling

2. **Function Registration**: Update both systems to register the new tool
   - Add tool definition to DO Functions agent configuration
   - Ensure both chat and Slack interfaces can access the tool

This pattern ensures tool parity between chat and Slack interfaces while maintaining clean separation of concerns and eliminating shared code dependencies.

**Example: Airtable Leads Tool**
```python
# /agent/functions/packages/gator/airtable_leads/__main__.py - DO Function
from airtable_leads import create_airtable_lead

def main(event, context):
    try:
        result = create_airtable_lead(
            event.get('customer'), 
            event.get('website'), 
            event.get('notes')
        )
        return {'statusCode': 200, 'body': result}
    except Exception as e:
        return {'statusCode': 500, 'body': {'error': str(e)}}

# /agent/functions/packages/gator/airtable_leads/airtable_leads.py - Business Logic
def create_airtable_lead(customer: str, website: str, notes: str) -> Dict[str, Any]:
    # Self-contained implementation with Airtable API calls
    # All business logic contained within function package
    return result

# Both chat and Slack interfaces use the same DO Function
# via HTTP calls, ensuring consistent behavior across platforms
```

### Database Safety
- Only read-only queries (SELECT, WITH) are allowed
- All queries are validated before execution
- Results are automatically serialized to JSON-compatible formats
- Connection timeouts and row limits are enforced
- Sample data mode uses SQLite for local development without external dependencies

### Streaming Implementation
- Chat uses native `fetch()` with `ReadableStream` processing
- Slack uses event-driven responses
- Both implementations handle backpressure and error states

### State Management
- Chat state is managed through Svelte stores
- Slack state is handled by FastAPI backend
- All state changes are reactive and typed

## API Endpoints

### Chat Backend
- `POST /api/chat/stream` - Stream chat responses as JSON lines
- `GET /health` - Health check with configuration status
- `GET /` - API documentation and endpoint listing


### DigitalOcean Functions
- `run_sql_query` - Execute database queries (production or sample data)
- `web_search` - Search the web for information
- `add_airtable_lead` - Create new lead records in Airtable database
- `list_airtable_leads` - Retrieve recent leads from Airtable for pipeline review
- `get_latest_workspaces` - Get recent workspace installations (demo-optimized)

## Deployment

### Chat Interface
1. **Build static site**: `npm run build`
2. **Deploy to DigitalOcean App Platform** as static site
3. **Set environment variables** in App Platform dashboard
4. **Deploy backend** separately as Python service


### DigitalOcean Functions
1. **Configure project.yml** with environment variables
2. **Deploy with**: `doctl serverless deploy . --remote-build`
3. **Test functions** via DigitalOcean Functions dashboard

## Security Considerations

### Database Access
- Read-only queries enforced at SQL parsing level
- Connection strings use SSL mode required
- Query timeouts prevent long-running operations
- Result set limits prevent memory exhaustion

### API Security
- CORS configured for development and production origins
- Input validation on all endpoints
- Error messages sanitized to prevent information disclosure

### Environment Variables
- All sensitive data stored in environment variables
- Development and production configurations separated
- API keys validated on service startup

## Troubleshooting

### Common Issues
1. **Database connection failures**: Check `DATABASE_URL` format and SSL requirements
2. **CORS errors**: Verify frontend URL is in backend CORS allowlist
3. **Function deployment failures**: Ensure all environment variables are set in project.yml
5. **Build failures**: Run `npm run check` for TypeScript errors

### Development Tips
1. **Use health endpoints** to verify service configuration
2. **Check browser developer tools** for streaming connection issues
3. **Monitor function logs** in DigitalOcean dashboard for serverless debugging
4. **Test database queries** locally before deployment

## Contributing

1. **Fork the repository** and create feature branch
2. **Test locally** with all services running
3. **Run type checking**: `npm run check` for frontend
4. **Verify database functions** work with test queries
5. **Submit pull request** with clear description of changes

This project demonstrates a complete AI agent implementation with multiple interfaces, self-contained serverless functions, and production-ready deployment patterns suitable for business intelligence applications.