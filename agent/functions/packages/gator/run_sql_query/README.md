# SQL Query Function

## Function Instructions

Execute read-only SQL queries against Gator database (Slack scheduling app).

TABLES & COLUMNS:
workspaces_workspace: id, slack_id, name, email_domain, enterprise_name, account_id, uninstalled, pending_deletion, created, updated
workspaces_gatoruser: id, slack_id, workspace_id, revoked, always_deliver_early, omit_gator_annotation, custom_delivery_time, created, updated  
later_messages_message: id, gator_id, sender_id, channel, status, scheduled_delivery, delivered, disable_early_delivery, im_recipient, created, updated

EXAMPLES:
- Count users: SELECT COUNT(*) FROM workspaces_gatoruser
- Workspaces added Dec 2023: SELECT COUNT(*) FROM workspaces_workspace WHERE created >= '2023-12-01' AND created < '2024-01-01'
- Scheduled messages: SELECT COUNT(*) FROM later_messages_message WHERE status = 'SCH'

The function only accepts SELECT queries for security. Results limited to 1000 rows. Use for business metrics, customer data, usage patterns, and analytics.

## Input Schema (OpenAPI)

```json
{
  "parameters": [
    {
      "in": "query",  
      "name": "query",
      "schema": {
        "type": "string"
      },
      "required": true,
      "description": "A read-only SQL SELECT query to execute against the database. Can include JOINs, WHERE clauses, GROUP BY, ORDER BY, and CTEs (WITH clauses). Must not contain INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE, GRANT, or REVOKE statements."
    }
  ]
}
```

## Output Schema (OpenAPI)

```json
{
  "properties": [
    {
      "name": "columns",
      "type": "array",
      "description": "Array of column names returned by the query"
    },
    {
      "name": "rows",
      "type": "array", 
      "description": "Array of row objects, where each object has keys corresponding to the column names and values containing the data. All PostgreSQL types are converted to JSON-compatible formats (dates as ISO strings, decimals as numbers)"
    },
    {
      "name": "row_count",
      "type": "number",
      "description": "The number of rows returned"
    },
    {
      "name": "truncated",
      "type": "boolean",
      "description": "True if results were truncated to 1000 rows, false otherwise"
    },
    {
      "name": "message",
      "type": "string",
      "description": "Optional message, present when results are truncated"
    }
  ]
}
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string

## Testing

```bash
cd functions/packages/gator/run_sql_query
export DATABASE_URL='postgresql://user:password@host:port/dbname?sslmode=require'
python test_local.py
```