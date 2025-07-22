import os
import requests
from typing import Dict, Any, List


def list_airtable_leads(max_records: int = 100, sort_field: str = 'Created', sort_direction: str = 'desc') -> Dict[str, Any]:
    """
    List all lead records from Airtable database.
    
    Args:
        max_records: Maximum number of records to return (default 100, max 1000)
        sort_field: Field to sort by (default 'Created')
        sort_direction: Sort direction - 'asc' or 'desc' (default 'desc')
        
    Returns:
        Dictionary with:
        - success: True if retrieval was successful
        - records: List of lead records with their details
        - count: Number of records returned
        - error: Error message if retrieval failed
    """
    # Get environment variables
    access_token = os.environ.get('AIRTABLE_ACCESS_TOKEN')
    base_id = os.environ.get('AIRTABLE_BASE_ID')
    table_id = os.environ.get('AIRTABLE_TABLE_ID')
    
    # Validate environment variables
    if not access_token:
        return {'error': 'AIRTABLE_ACCESS_TOKEN environment variable not configured'}
    if not base_id:
        return {'error': 'AIRTABLE_BASE_ID environment variable not configured'}
    if not table_id:
        return {'error': 'AIRTABLE_TABLE_ID environment variable not configured'}
    
    # Construct Airtable API URL
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    
    # Set up headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Set up query parameters
    params = {
        'maxRecords': max_records,
        'view': 'Grid view'  # Use default grid view
    }
    
    # Add sorting if specified
    if sort_field:
        # Airtable expects sort as array of objects
        sort_param = [{
            'field': sort_field,
            'direction': sort_direction
        }]
        # Convert to URL parameter format
        params['sort[0][field]'] = sort_field
        params['sort[0][direction]'] = sort_direction
    
    try:
        # Make request to Airtable API
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        # Handle different response status codes
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            
            # Process records to extract fields
            processed_records = []
            for record in records:
                fields = record.get('fields', {})
                processed_record = {
                    'id': record.get('id'),
                    'customer': fields.get('Customer', ''),
                    'website': fields.get('Website', ''),
                    'notes': fields.get('Notes', ''),
                    'created': fields.get('Created', ''),
                    'last_modified': fields.get('Last Modified', '')
                }
                processed_records.append(processed_record)
            
            return {
                'success': True,
                'records': processed_records,
                'count': len(processed_records),
                'message': f'Successfully retrieved {len(processed_records)} lead records'
            }
            
        elif response.status_code == 401:
            return {'error': 'Airtable authentication failed. Check your access token.'}
        elif response.status_code == 403:
            return {'error': 'Airtable access forbidden. Check permissions for this base/table.'}
        elif response.status_code == 404:
            return {'error': 'Airtable base or table not found. Check your base and table IDs.'}
        elif response.status_code == 422:
            error_detail = response.json().get('error', {}).get('message', 'Invalid parameters')
            return {'error': f'Airtable validation error: {error_detail}'}
        else:
            return {'error': f'Airtable request failed with status {response.status_code}'}
            
    except requests.exceptions.Timeout:
        return {'error': 'Airtable request timed out after 30 seconds'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Network error: Could not connect to Airtable'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Network error: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}