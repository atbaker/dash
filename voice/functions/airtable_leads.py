import os
import requests
from pipecat.services.llm_service import FunctionCallParams


async def airtable_leads(params: FunctionCallParams):
    """
    Create a new lead record in Airtable by calling DigitalOcean Function via HTTP.
    
    This is the HTTP wrapper for the DigitalOcean Functions implementation.
    """
    try:
        # Extract parameters from function call
        customer = params.arguments.get('customer')
        website = params.arguments.get('website')
        notes = params.arguments.get('notes')
        
        # Validate required parameters
        if not customer:
            await params.result_callback({"error": "Customer parameter is required"})
            return
            
        if not website:
            await params.result_callback({"error": "Website parameter is required"})
            return
            
        if not notes:
            await params.result_callback({"error": "Notes parameter is required"})
            return
        
        # Get DigitalOcean Functions base URL
        base_url = os.environ.get('DO_FUNCTIONS_BASE_URL')
        
        if not base_url:
            await params.result_callback({"error": "DO_FUNCTIONS_BASE_URL environment variable not configured"})
            return
        
        # Make HTTP request to DigitalOcean Function
        function_url = f"{base_url}/airtable_leads"
        
        response = requests.post(
            function_url,
            json={
                "customer": customer,
                "website": website,
                "notes": notes
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
        await params.result_callback({"error": "Airtable leads request timed out"})
    except requests.exceptions.RequestException as e:
        await params.result_callback({"error": "Network error", "details": str(e)})
    except Exception as e:
        await params.result_callback({"error": f"Airtable leads error: {str(e)}"})