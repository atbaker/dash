# Airtable Leads Function

## Function Instructions

Create new lead record in Airtable database for promising Gator customers. Use after researching company with web search to qualify leads.

PARAMETERS:
- customer: Name of Slack workspace/company (required)  
- website: Company website URL (required)
- notes: LLM-authored insights about company (required)

Creates record with Customer, Website, Notes fields. Created date auto-populated by Airtable.

Use for sales follow-up workflow: query recent Gator installs → research company → create qualified lead entry.

## Input Schema (OpenAPI)

```json
{
  "parameters": [
    {
      "in": "query",
      "name": "customer",
      "schema": {
        "type": "string"
      },
      "required": true,
      "description": "Name of the Slack workspace or company that installed Gator"
    },
    {
      "in": "query",
      "name": "website", 
      "schema": {
        "type": "string"
      },
      "required": true,
      "description": "Company website URL"
    },
    {
      "in": "query",
      "name": "notes",
      "schema": {
        "type": "string"
      },
      "required": true,
      "description": "LLM-authored notes and insights about the company based on research"
    }
  ]
}
```

## Output Schema (OpenAPI)

```json
{
  "properties": [
    {
      "name": "success",
      "type": "boolean",
      "description": "True if record was created successfully"
    },
    {
      "name": "record_id",
      "type": "string",
      "description": "Airtable record ID of the created lead entry"
    },
    {
      "name": "customer",
      "type": "string",
      "description": "Customer name that was stored"
    },
    {
      "name": "website",
      "type": "string", 
      "description": "Website URL that was stored"
    },
    {
      "name": "created_time",
      "type": "string",
      "description": "ISO timestamp when record was created"
    },
    {
      "name": "message",
      "type": "string",
      "description": "Success message"
    },
    {
      "name": "error",
      "type": "string",
      "description": "Error message if creation failed"
    }
  ]
}
```

## Environment Variables

- `AIRTABLE_ACCESS_TOKEN`: Personal Access Token for Airtable API
- `AIRTABLE_BASE_ID`: Base ID for the Gator leads database
- `AIRTABLE_TABLE_ID`: Table ID for the leads table (e.g., tblF8FXwSSyr3pXv4)

## Testing

```bash
cd functions/packages/gator/airtable_leads
export AIRTABLE_ACCESS_TOKEN='your_token_here'
export AIRTABLE_BASE_ID='your_base_id_here'
export AIRTABLE_TABLE_ID='your_table_id_here'
python test_local.py
```