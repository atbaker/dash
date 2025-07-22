# List Airtable Leads Function

## Function Instructions

Retrieve the 10 most recent lead records from Airtable database to review qualified leads and sales pipeline. Use at the end of lead qualification workflow to show all accumulated leads.

NO PARAMETERS REQUIRED - Returns a fixed set of the 10 most recent lead records sorted by creation date.

Returns list of lead records with Customer, Website, Notes, Created date, and Last Modified date.

Use for sales review workflow: query recent installs → research companies → create leads → review all leads.

## Input Schema (OpenAPI)

```json
{
  "parameters": []
}
```

## Output Schema (OpenAPI)

```json
{
  "properties": [
    {
      "name": "success",
      "type": "boolean",
      "description": "True if records were retrieved successfully"
    },
    {
      "name": "records",
      "type": "array",
      "description": "Array of lead records",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Airtable record ID"
          },
          "customer": {
            "type": "string",
            "description": "Customer/workspace name"
          },
          "website": {
            "type": "string",
            "description": "Company website URL"
          },
          "notes": {
            "type": "string",
            "description": "LLM-authored insights about the company"
          },
          "created": {
            "type": "string",
            "description": "ISO timestamp when record was created"
          },
          "last_modified": {
            "type": "string",
            "description": "ISO timestamp when record was last modified"
          }
        }
      }
    },
    {
      "name": "count",
      "type": "integer",
      "description": "Number of records returned"
    },
    {
      "name": "message",
      "type": "string",
      "description": "Success message with count"
    },
    {
      "name": "error",
      "type": "string",
      "description": "Error message if retrieval failed"
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
cd functions/packages/gator/list_airtable_leads
export AIRTABLE_ACCESS_TOKEN='your_token_here'
export AIRTABLE_BASE_ID='your_base_id_here'
export AIRTABLE_TABLE_ID='your_table_id_here'
python test_local.py
```