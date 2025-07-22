import os
import requests
from pipecat.services.llm_service import FunctionCallParams


async def list_airtable_leads(params: FunctionCallParams):
    """
    List all lead records from Airtable by calling DigitalOcean Function via HTTP.
    
    This is the HTTP wrapper for the DigitalOcean Functions implementation.
    """
    try:
        # Extract optional parameters from function call
        max_records = params.arguments.get('max_records', 100)
        sort_field = params.arguments.get('sort_field', 'Created')
        sort_direction = params.arguments.get('sort_direction', 'desc')
        
        # Get DigitalOcean Functions base URL
        base_url = os.environ.get('DO_FUNCTIONS_BASE_URL')
        
        if not base_url:
            await params.result_callback({"error": "DO_FUNCTIONS_BASE_URL environment variable not configured"})
            return
        
        # Make HTTP request to DigitalOcean Function
        function_url = f"{base_url}/list_airtable_leads"
        
        response = requests.post(
            function_url,
            json={
                "max_records": max_records,
                "sort_field": sort_field,
                "sort_direction": sort_direction
            },
            timeout=30
        )
        
        if response.status_code == 200:
            # Success - return the function result
            result = response.json()
            await params.result_callback(result.get('body', result))
        else:
            # Error - return the error information
            try:
                error_data = response.json()
                await params.result_callback(error_data.get('body', error_data))
            except:
                await params.result_callback({
                    "error": f"HTTP {response.status_code}: {response.text}"
                })
        
    except requests.exceptions.Timeout:
        await params.result_callback({"error": "List Airtable leads request timed out"})
    except requests.exceptions.RequestException as e:
        await params.result_callback({"error": "Network error", "details": str(e)})
    except Exception as e:
        await params.result_callback({"error": f"List Airtable leads error: {str(e)}"})