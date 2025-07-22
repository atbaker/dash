"""
Business logic for getting the latest workspaces.
"""
import requests
from typing import Dict, Any


def get_latest_workspaces(functions_base_url: str) -> Dict[str, Any]:
    """
    Get the 10 most recent workspaces by leveraging the run_sql_query function.
    
    Retrieves workspace names, install dates, and domain names from the
    workspaces_workspace table, ordered by creation date (most recent first).
    
    Args:
        functions_base_url (str): Base URL for DigitalOcean Functions
        
    Returns:
        Dict[str, Any]: Query results with workspace information
        
    Raises:
        requests.RequestException: If the HTTP request fails
        Exception: For other errors during processing
    """
    
    # SQL query to get the 10 most recent workspaces
    # Based on schema: name, email_domain (domain), created (install date)
    sql_query = """
    SELECT 
        name,
        email_domain as domain,
        created as install_date,
        slack_id,
        enterprise_name
    FROM workspaces_workspace 
    WHERE uninstalled = FALSE 
      AND pending_deletion = FALSE
    ORDER BY created DESC 
    LIMIT 10
    """
    
    # Make HTTP request to run_sql_query function
    response = requests.post(
        f"{functions_base_url}/run_sql_query",
        json={"query": sql_query},
        timeout=60  # Allow extra time for query execution
    )
    
    # Check if request was successful
    response.raise_for_status()
    
    # Parse response
    result = response.json()
    
    # Debug: print the actual response for troubleshooting
    print(f"DEBUG: run_sql_query response: {result}")
    
    # The run_sql_query function returns the query results directly,
    # not wrapped in a DigitalOcean Function response format
    if 'error' in result:
        error_msg = result.get('error', 'Unknown error from run_sql_query')
        raise Exception(f"SQL query failed: {error_msg}")
    
    # Use the result directly as query results
    query_results = result
    
    # Add context information for better demo presentation
    workspace_data = {
        'query_description': 'Latest 10 workspaces ordered by install date',
        'total_count': query_results.get('row_count', 0),
        'truncated': query_results.get('truncated', False),
        'workspaces': query_results.get('rows', []),
        'columns': query_results.get('columns', [])
    }
    
    return workspace_data