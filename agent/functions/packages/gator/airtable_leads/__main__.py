import os
import requests
from airtable_leads import create_airtable_lead


def main(event, context):
    """
    Create a new lead record in Airtable database.
    
    This is the DigitalOcean Functions adapter for the shared Airtable leads logic.
    """
    try:
        # Validate event structure
        if not event:
            return {
                'statusCode': 400,
                'body': {'error': 'Event data is required'}
            }
        
        # Extract parameters from event
        customer = event.get('customer')
        website = event.get('website') 
        notes = event.get('notes')
        
        if not customer:
            return {
                'statusCode': 400,
                'body': {'error': 'Customer parameter is required'}
            }
            
        if not website:
            return {
                'statusCode': 400,
                'body': {'error': 'Website parameter is required'}
            }
            
        if not notes:
            return {
                'statusCode': 400,
                'body': {'error': 'Notes parameter is required'}
            }
        
        # Execute Airtable creation using shared function
        result = create_airtable_lead(customer, website, notes)
        
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