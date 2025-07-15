import os
import requests
from web_search import search_web


def main(event, context):
    """
    Perform web search using Brave Search API.
    
    This is the DigitalOcean Functions adapter for the shared web search logic.
    """
    try:
        # Extract query from event
        if not event or 'query' not in event:
            return {
                'statusCode': 400,
                'body': {'error': 'Query parameter is required'}
            }
        
        query = event['query']
        
        # Execute search using shared function
        result = search_web(query)
        
        # Return appropriate status code based on result
        if 'error' in result:
            status_code = 500
            if 'timed out' in result['error']:
                status_code = 408
            elif 'API error' in result['error']:
                status_code = 500
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
            'body': {'error': 'Search request timed out'}
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': {'error': 'Network error', 'details': str(e)}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': f'Internal error: {str(e)}'}
        }