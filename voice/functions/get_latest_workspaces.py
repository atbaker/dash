import os
import requests
from pipecat.services.llm_service import FunctionCallParams


async def get_latest_workspaces(params: FunctionCallParams):
    """
    Get the 10 most recent workspace installations by calling DigitalOcean Function via HTTP.
    
    This is the HTTP wrapper for the DigitalOcean Functions implementation.
    No parameters required - returns 10 most recent active workspaces.
    """
    try:
        # Get DigitalOcean Functions base URL
        base_url = os.environ.get('DO_FUNCTIONS_BASE_URL')
        
        if not base_url:
            await params.result_callback({"error": "DO_FUNCTIONS_BASE_URL environment variable not configured"})
            return
        
        # Make HTTP request to DigitalOcean Function (no parameters needed)
        function_url = f"{base_url}/get_latest_workspaces"
        
        response = requests.post(
            function_url,
            json={},  # Empty payload since no parameters are needed
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
        await params.result_callback({"error": "Get latest workspaces request timed out"})
    except requests.exceptions.RequestException as e:
        await params.result_callback({"error": "Network error", "details": str(e)})
    except Exception as e:
        await params.result_callback({"error": f"Get latest workspaces error: {str(e)}"})