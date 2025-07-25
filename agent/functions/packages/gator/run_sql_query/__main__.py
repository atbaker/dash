import os
import psycopg
from db_utils import execute_read_only_query


def main(event, context):
    """
    Execute a read-only SQL query against the production database.
    
    This is the DigitalOcean Functions adapter for the shared query execution logic.
    """
    try:
        # Extract query from event
        if not event or 'query' not in event:
            return {
                'statusCode': 400,
                'body': {'error': 'Query parameter is required'}
            }
        
        query = event['query']
        
        # Get database connection string from environment variable
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            return {
                'statusCode': 500,
                'body': {'error': 'DATABASE_URL environment variable not configured'}
            }
        
        # Execute query using shared utility
        result = execute_read_only_query(query, database_url)
        
        return {
            'statusCode': 200,
            'body': result
        }
        
    except ValueError as e:
        # Query validation errors
        return {
            'statusCode': 403,
            'body': {'error': str(e)}
        }
    except psycopg.OperationalError as e:
        return {
            'statusCode': 503,
            'body': {'error': 'Database connection failed', 'details': str(e)}
        }
    except psycopg.ProgrammingError as e:
        return {
            'statusCode': 400,
            'body': {'error': 'Query error', 'details': str(e)}
        }
    except psycopg.Error as e:
        return {
            'statusCode': 500,
            'body': {'error': 'Database error', 'details': str(e)}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': f'Internal error: {str(e)}'}
        }