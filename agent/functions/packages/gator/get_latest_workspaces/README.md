# Latest Workspaces Function

## Function Instructions

Get the 10 most recent workspaces from the Gator database (Slack scheduling app). This function is specifically designed for demo purposes to provide reliable workspace data without the risk of LLM-generated SQL errors.

The function returns workspace information including:
- **name** - Workspace name
- **domain** - Email domain associated with the workspace  
- **install_date** - When the workspace was created/installed
- **slack_id** - Slack workspace identifier
- **enterprise_name** - Enterprise/organization name

This function leverages the existing `run_sql_query` function by making HTTP calls with a predefined, validated SQL query. Use this function when you need to show recent workspace installations for demos or when you want reliable workspace data without query generation risks.

The function automatically filters out uninstalled and pending deletion workspaces, returning only active installations ordered by most recent first.

## Input Schema (OpenAPI)

```json
{
  "parameters": []
}
```

*Note: This function requires no input parameters - it always returns the 10 most recent workspaces.*

## Output Schema (OpenAPI)

```json
{
  "properties": [
    {
      "name": "query_description",
      "type": "string",
      "description": "Human-readable description of the query executed"
    },
    {
      "name": "total_count",
      "type": "number",
      "description": "The number of workspaces returned"
    },
    {
      "name": "truncated",
      "type": "boolean",
      "description": "Whether the results were truncated (always false for this function since we limit to 10)"
    },
    {
      "name": "workspaces",
      "type": "array",
      "description": "Array of workspace objects, each containing name, domain, install_date, slack_id, and enterprise_name"
    },
    {
      "name": "columns",
      "type": "array",
      "description": "Array of column names in the workspace objects"
    }
  ]
}
```

## Environment Variables

- `DO_FUNCTIONS_BASE_URL`: Base URL for calling other DigitalOcean Functions (specifically run_sql_query)

## Testing

```bash
cd functions/packages/gator/get_latest_workspaces
pip install requests
export DO_FUNCTIONS_BASE_URL='https://faas-xxx.doserverless.co/api/v1/web/fn-xxx/gator'
python test_local.py
```

## Implementation Details

- Executes predefined SQL query via HTTP call to `run_sql_query` function
- Filters active workspaces only (uninstalled=FALSE, pending_deletion=FALSE)
- Orders by creation date descending (most recent first)
- Limited to 10 results for demo purposes
- 60-second timeout for HTTP requests