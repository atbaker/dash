# Slack Bot Integration for DASH AI Assistant

## Overview

The DASH AI assistant now includes a Slack bot interface that allows users to interact with the AI agent directly through Slack. The bot supports:

- Direct messages (DMs) with the bot
- Channel mentions (`@DASH AI`)
- Threaded conversations for context
- Full conversation history retrieval from Slack

## Setup Instructions

### 1. Install Dependencies

```bash
cd chat/backend
uv sync
```

### 2. Create Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From an app manifest"
3. Select your workspace
4. Copy and paste the contents of `slack_manifest.yml`
5. Click "Create"

### 3. Get Slack Credentials

After creating the app, you'll need:

- **Bot User OAuth Token**: Go to "OAuth & Permissions" → copy the "Bot User OAuth Token" (starts with `xoxb-`)
- **Signing Secret**: Go to "Basic Information" → "App Credentials" → copy the "Signing Secret"

### 4. Configure Environment Variables

Add these to your `.env` file:

```env
# Existing DASH configuration
DO_AGENT_ENDPOINT=https://your-agent-endpoint
DO_AGENT_ACCESS_KEY=your-access-key
DEBUG=true

# Slack configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
```

### 5. Update Slack App Settings

1. Go to "Event Subscriptions" in your Slack app settings
2. Enable events and set the Request URL to: `https://your-domain.com/slack/events`
3. Subscribe to these bot events:
   - `app_mention`
   - `message.im`
4. Save changes

### 6. Install App to Workspace

1. Go to "Install App" in your Slack app settings
2. Click "Install to Workspace"
3. Grant the requested permissions

## Usage

### Direct Messages
Users can DM the bot directly:
```
User: What's our revenue this quarter?
DASH AI: Based on the latest data, your Q4 revenue is...
```

### Channel Mentions
Users can mention the bot in channels:
```
User: @DASH AI can you analyze our customer growth?
DASH AI: I'll analyze your customer growth data...
```

### Threaded Conversations
The bot maintains context in threaded conversations and uses Slack's native conversation history.

## Architecture

### File Structure
```
chat/backend/
├── main.py                     # FastAPI app with Slack endpoints
├── slack_bot.py                # Slack event handling and API integration
├── chat_service.py             # Shared DigitalOcean Agent logic
├── slack_manifest.yml          # Slack app configuration
└── test_slack_integration.py   # Basic integration tests
```

### Key Components

- **SlackBot**: Handles Slack events, message parsing, and conversation history
- **chat_service**: Shared logic for communicating with DigitalOcean Agent
- **Slack endpoints**: `/slack/events` for receiving Slack event callbacks

### Conversation History

The bot uses Slack's native conversation storage:
- **DMs**: `conversations.history` API to get message history
- **Channels**: `conversations.replies` API for threaded context
- Converts Slack message format to OpenAI format before sending to DigitalOcean Agent

## Testing

Run the integration test:
```bash
uv run python test_slack_integration.py
```

## Deployment

1. **Update your domain**: Modify the Request URL in Slack app settings to point to your production domain
2. **Set production environment variables**: Ensure `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` are configured
3. **Deploy**: Use your existing deployment process for the FastAPI backend

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check that the Request URL is accessible and returns 200 OK
2. **Authentication errors**: Verify `SLACK_SIGNING_SECRET` matches your app settings
3. **Permission errors**: Ensure bot has required OAuth scopes (see `slack_manifest.yml`)

### Debugging

1. **Check logs**: Bot errors are logged to stdout
2. **Test endpoints**: Visit `/health` to check if Slack integration is enabled
3. **Verify signatures**: The bot validates all incoming Slack requests

### Health Check

The `/health` endpoint now includes Slack status:
```json
{
  "status": "healthy",
  "config": {"has_endpoint": true},
  "slack_enabled": true
}
```

## Security

- All Slack requests are verified using HMAC signature validation
- Bot only processes messages from authenticated Slack workspaces
- No sensitive information is logged or stored locally