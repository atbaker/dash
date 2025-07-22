import os
from get_latest_workspaces import get_latest_workspaces


def main(event, context):
    """
    Get the 10 most recent workspaces from the workspaces_workspace table.
    
    This function leverages the existing run_sql_query function to execute
    a predefined query that retrieves workspace names, install dates, and domains.
    """
    try:
        # Get the base URL for other DigitalOcean Functions
        functions_base_url = os.environ.get('DO_FUNCTIONS_BASE_URL')
        
        if not functions_base_url:
            return {
                'statusCode': 500,
                'body': {'error': 'DO_FUNCTIONS_BASE_URL environment variable not configured'}
            }
        
        # Call the business logic function
        result = get_latest_workspaces(functions_base_url)
        
        return {
            'statusCode': 200,
            'body': result
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': f'Internal error: {str(e)}'}
        }