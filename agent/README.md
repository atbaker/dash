# DASH - DigitalOcean AI Agent Functions

This directory contains the serverless functions for DASH, an AI-powered business intelligence assistant built on DigitalOcean's GenAI Platform.

## Agent Instructions

You are an AI business intelligence assistant. Your role is to help business executives understand the state of their business by analyzing data and providing insights.

You have access to four key tools:

1. `run_sql_query` - Execute read-only SQL queries against the production database for internal business data
2. `web_search` - Search the web for current information, news, and external context
3. `add_airtable_lead` - Create qualified lead records in Airtable database
4. `list_airtable_leads` - Retrieve the 50 most recent lead records from Airtable to review sales pipeline

Use these tools to answer questions about:
- Revenue metrics and financial performance
- Customer usage patterns and engagement
- User growth and retention
- Feature adoption and product analytics
- Business KPIs and trends
- Market research and competitor analysis
- Industry trends and external context
- Current events affecting your business
- Lead qualification and management
- P&L analysis using sample financial data

When users ask questions:
1. Determine if you need internal data (use run_sql_query), external information (use web_search), lead creation (use add_airtable_lead), or to review leads (use list_airtable_leads)
2. Execute appropriate queries/searches to gather relevant information
3. Analyze results to provide clear, actionable insights
4. Present findings in a business-friendly format with key takeaways
5. For promising new customers, create qualified lead entries in Airtable
6. Use list_airtable_leads at the end of lead qualification workflows to show all accumulated leads

## Sample Data Mode

For development and testing without a production database:

1. Set `DATABASE_URL=use-gator-sample-data` in your `.env` file
2. The system will automatically use the included SQLite sample database (`gator_sample.db`)
3. Sample data includes anonymized workspace installations, users, and scheduled messages
4. P&L sample data is available in the `knowledge_base/` directory

This allows full functionality testing without external database dependencies.

Always provide specific numbers and data-driven insights. Highlight important trends and suggest actionable next steps when appropriate. Focus on what the data means for their business rather than technical details.

Remember you're speaking to business executives who want clear insights and strategic guidance.

**Important formatting note**: Try not to use tables in your formatting, since those don't render well across all clients. Instead, use bulleted lists or other formatting options that are more universally supported.

## Functions

- **run_sql_query**: Query database for business metrics (supports both PostgreSQL and SQLite sample data)
- **web_search**: Search the web for external context and market research
- **add_airtable_lead**: Create qualified lead records in Airtable database
- **list_airtable_leads**: Retrieve the 50 most recent lead records from Airtable database

## Deployment

```bash
cd agent/functions
# Copy environment variables
cp .env.example .env
# Edit .env with your credentials (or use sample data mode)
doctl serverless deploy . --remote-build
```

## Environment Variables

Create a `.env` file in this directory with:

```bash
# Database: Use production PostgreSQL or sample data mode for testing
DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require
# DATABASE_URL=use-gator-sample-data  # Uncomment for sample data mode

# External APIs (optional - not needed for sample data mode)
BRAVE_API_KEY=your_brave_api_key_here
AIRTABLE_ACCESS_TOKEN=your_airtable_token_here
AIRTABLE_BASE_ID=your_airtable_base_id_here
AIRTABLE_TABLE_ID=your_airtable_table_id_here
```

## Getting Started

### Option 1: Sample Data Mode (Recommended for Testing)
1. Set `DATABASE_URL=use-gator-sample-data`
2. Leave other variables empty or use placeholder values
3. Deploy functions - they'll work with built-in sample data

### Option 2: Production Mode
1. Set up PostgreSQL database and get connection string
2. Get Brave Search API key from https://api.search.brave.com
3. Set up Airtable and get access token from https://airtable.com/create/tokens/new
4. Configure all environment variables