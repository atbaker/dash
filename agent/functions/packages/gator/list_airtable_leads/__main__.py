import os
import requests
from list_airtable_leads import list_airtable_leads


def main(event, context):
    """
    List all lead records from Airtable database.
    
    This is the DigitalOcean Functions adapter for listing Airtable leads.
    """
    try:
        # Extract optional parameters from event
        max_records = event.get('max_records', 100) if event else 100
        sort_field = event.get('sort_field', 'Created') if event else 'Created'
        sort_direction = event.get('sort_direction', 'desc') if event else 'desc'
        
        # Validate max_records
        if not isinstance(max_records, int) or max_records < 1:
            return {
                'statusCode': 400,
                'body': {'error': 'max_records must be a positive integer'}
            }
        
        # Cap max_records to prevent excessive data retrieval
        if max_records > 1000:
            max_records = 1000
        
        # Execute Airtable listing using shared function
        result = list_airtable_leads(max_records, sort_field, sort_direction)
        
        # Return appropriate status code based on result
        if 'error' in result:
            # Determine appropriate HTTP status code
            if 'not configured' in result['error']:
                status_code = 500  # Server configuration error
            elif 'authentication failed' in result['error']:
                status_code = 401  # Unauthorized
            elif 'access forbidden' in result['error']:
                status_code = 403  # Forbidden
            elif 'not found' in result['error']:
                status_code = 404  # Not found
            elif 'validation error' in result['error']:
                status_code = 422  # Unprocessable entity
            elif 'timed out' in result['error']:
                status_code = 408  # Request timeout
            elif 'Network error' in result['error']:
                status_code = 502  # Bad gateway
            else:
                status_code = 500  # Internal server error
                
            return {
                'statusCode': status_code,
                'body': result
            }
        else:
            return {
                'statusCode': 200,
                'body': result
            }
            
    except requests.exceptions.Timeout:
        return {
            'statusCode': 408,
            'body': {'error': 'Airtable request timed out'}
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 502,
            'body': {'error': 'Network error', 'details': str(e)}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': f'Internal error: {str(e)}'}
        }