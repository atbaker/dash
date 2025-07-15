"""
Shared Airtable leads functionality for creating new lead records.
Works with both Pipecat voice agent and DigitalOcean Functions.
"""
import os
import requests
from typing import Dict, Any, Optional


def create_airtable_lead(
    customer: str, 
    website: str, 
    notes: str, 
    api_key: Optional[str] = None, 
    base_id: Optional[str] = None,
    table_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new lead record in Airtable database.
    
    Args:
        customer: Name of the Slack workspace/company
        website: Company website URL  
        notes: LLM-authored notes about the company
        api_key: Airtable Personal Access Token (optional, will use environment variable if not provided)
        base_id: Airtable base ID (optional, will use environment variable if not provided)
        table_id: Airtable table ID (optional, will use environment variable if not provided)
    
    Returns:
        Dictionary containing creation result or error information
    """
    try:
        # Validate required parameters
        if not customer or not customer.strip():
            return {'error': 'Customer parameter is required'}
        
        if not website or not website.strip():
            return {'error': 'Website parameter is required'}
            
        if not notes or not notes.strip():
            return {'error': 'Notes parameter is required'}
        
        # Get API key from parameter or environment variable
        if not api_key:
            api_key = os.environ.get('AIRTABLE_ACCESS_TOKEN')
        
        if not api_key:
            return {'error': 'Airtable access token not configured'}
        
        # Get base ID from parameter or environment variable
        if not base_id:
            base_id = os.environ.get('AIRTABLE_BASE_ID')
            
        if not base_id:
            return {'error': 'Airtable base ID not configured'}
        
        # Get table ID from parameter or environment variable
        if not table_id:
            table_id = os.environ.get('AIRTABLE_TABLE_ID')
            
        if not table_id:
            return {'error': 'Airtable table ID not configured'}
        
        # Set up request parameters
        url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Prepare request body with the lead data
        body = {
            "fields": {
                "Customer": customer.strip(),
                "Website": website.strip(),
                "Notes": notes.strip()
                # Created field is auto-populated by Airtable
            }
        }
        
        # Make API request
        response = requests.post(url, headers=headers, json=body, timeout=10)
        
        if response.status_code == 200:
            # Success - record created
            data = response.json()
            return {
                'success': True,
                'record_id': data.get('id'),
                'customer': customer,
                'website': website,
                'created_time': data.get('createdTime'),
                'message': f'Lead record created for {customer}'
            }
        elif response.status_code == 401:
            return {
                'error': 'Airtable authentication failed - check access token',
                'status_code': response.status_code
            }
        elif response.status_code == 403:
            return {
                'error': 'Airtable access forbidden - check token permissions and base access',
                'status_code': response.status_code
            }
        elif response.status_code == 404:
            return {
                'error': 'Airtable base or table not found - check base ID and table ID',
                'status_code': response.status_code
            }
        elif response.status_code == 422:
            return {
                'error': 'Airtable validation error - check field names and data types',
                'status_code': response.status_code,
                'details': response.text
            }
        else:
            return {
                'error': f'Airtable API error: {response.status_code}',
                'status_code': response.status_code,
                'details': response.text
            }
        
    except requests.exceptions.Timeout:
        return {'error': 'Airtable request timed out'}
    except requests.exceptions.RequestException as e:
        return {'error': 'Network error', 'details': str(e)}
    except Exception as e:
        return {'error': f'Internal error: {str(e)}'}