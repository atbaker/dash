# DASH Chat - Svelte Edition

A modern, reactive chat interface for DASH powered by DigitalOcean's GenAI Platform Agent, built with SvelteKit and Tailwind CSS.

## Features

- **Real-time streaming chat** using native fetch() and ReadableStream
- **Reactive UI** with Svelte 5 and automatic state management
- **Modern design** with Tailwind CSS 4.0
- **TypeScript support** for better development experience
- **Static site generation** for DigitalOcean App Platform deployment
- **Component-based architecture** for maintainability

## Architecture

- **Frontend**: SvelteKit 2.0 + Svelte 5 + Tailwind CSS 4.0
- **Backend**: FastAPI with JSON streaming endpoints
- **Deployment**: Static site generation for DigitalOcean App Platform
- **State Management**: Svelte stores with reactive updates
- **Streaming**: Native fetch() with ReadableStream processing

## Quick Start

### Prerequisites

- Node.js 18+ 
- Python 3.11+
- uv (for Python dependency management)

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:5173
```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
uv sync

# Copy environment variables
cp .env.example .env
# Edit .env with your DigitalOcean Agent credentials

# Start backend server
uv run python main.py

# Backend runs on http://localhost:8000
```

## Environment Variables

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Backend (backend/.env)
```env
DO_AGENT_ENDPOINT=https://your-agent-endpoint
DO_AGENT_ACCESS_KEY=your-access-key
DEBUG=true
```

## Project Structure

```
chat-svelte/
├── src/
│   ├── routes/
│   │   └── +page.svelte          # Main chat interface
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ChatMessage.svelte # Individual message component
│   │   │   ├── MessageList.svelte # Scrolling message container
│   │   │   └── ChatInput.svelte   # Input form with streaming
│   │   ├── stores/
│   │   │   └── chat.ts           # Svelte stores for state
│   │   └── api/
│   │       └── chat.ts           # API communication layer
│   ├── app.html                  # HTML template
│   └── app.css                   # Global styles with Tailwind
├── backend/
│   ├── main.py                   # FastAPI application
│   ├── pyproject.toml           # Python dependencies
│   └── .env.example             # Environment variables
├── static/                       # Static assets
├── svelte.config.js             # SvelteKit configuration
└── package.json                 # Node.js dependencies
```

## Development

### Frontend Development
```bash
npm run dev          # Start dev server with HMR
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development
```bash
cd backend
uv run python main.py    # Start FastAPI server with reload
```

### Type Checking
```bash
npm run check        # Run svelte-check for TypeScript
npm run check:watch  # Watch mode for type checking
```

## Deployment to DigitalOcean App Platform

### 1. Prepare for Deployment

The project is configured for static site generation:

```bash
npm run build
# Generates static files in build/ directory
```

### 2. DigitalOcean App Platform Setup

1. **Connect your GitHub repository** to DigitalOcean App Platform
2. **Configure the app**:
   - **Type**: Static Site
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Node Version**: 18+

3. **Environment Variables** in App Platform:
   - `VITE_API_BASE_URL`: Your backend API URL

### 3. Backend Deployment

Deploy the FastAPI backend separately:
- Use DigitalOcean App Platform with Python runtime
- Set environment variables for `DO_AGENT_ENDPOINT` and `DO_AGENT_ACCESS_KEY`

## How It Works

### Reactive State Management

The app uses Svelte stores for clean state management:

```typescript
// Add user message and start streaming
chatStore.addUserMessage(message);
const streamingId = chatStore.startAssistantMessage();

// Stream content updates reactively
chatStore.appendStreamingContent(chunk);

// Complete streaming
chatStore.completeStreaming();
```

### Streaming Implementation

Uses native browser APIs for efficient streaming:

```typescript
const response = await fetch('/api/chat/stream', {
  method: 'POST',
  body: JSON.stringify({ message })
});

const reader = response.body.getReader();
// Process stream chunks in real-time
```

### Component Architecture

- **ChatMessage.svelte**: Displays individual messages with animations
- **MessageList.svelte**: Manages scrolling and message list
- **ChatInput.svelte**: Handles user input with auto-resize and validation

## API Endpoints

### POST /api/chat/stream
Streams chat responses as JSON lines:

```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

Response format:
```json
{"content": "Hello"}
{"content": " there!"}
{"complete": true}
```

### GET /health
Health check endpoint:

```json
{
  "status": "healthy",
  "config": {
    "has_endpoint": true
  }
}
```

## Key Advantages Over HTMX Version

1. **Cleaner Streaming**: Native fetch() instead of SSE complexity
2. **Reactive Updates**: Automatic UI updates without manual DOM manipulation
3. **Better State Management**: Centralized state with Svelte stores
4. **Component Reusability**: Modular, testable components
5. **Modern Development**: Hot reload, TypeScript, modern build tools
6. **Easier Maintenance**: Clear separation of concerns

## Sample Chat Capabilities

The AI assistant can help with:
- **Business data queries** - Ask about workspaces, users, database info
- **Web search** - Search for latest information and news
- **Lead management** - Create qualified lead entries in Airtable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with both frontend and backend
5. Submit a pull request

## License

MIT License - see LICENSE file for details