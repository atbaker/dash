import os
import psycopg
import sqlite3
from db_utils import execute_read_only_query
from sqlite_utils import execute_read_only_query_sqlite


def main(event, context):
    """
    Execute a read-only SQL query against the database.
    
    Uses PostgreSQL if DATABASE_URL is configured, otherwise falls back to SQLite sample data.
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
        
        if database_url and database_url != 'use-gator-sample-data':
            # Use PostgreSQL production database
            try:
                result = execute_read_only_query(query, database_url)
                return {
                    'statusCode': 200,
                    'body': result
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
        else:
            # Use SQLite sample data fallback
            try:
                result = execute_read_only_query_sqlite(query)
                return {
                    'statusCode': 200,
                    'body': result
                }
            except sqlite3.Error as e:
                return {
                    'statusCode': 500,
                    'body': {'error': 'SQLite database error', 'details': str(e)}
                }
            except FileNotFoundError as e:
                return {
                    'statusCode': 500,
                    'body': {'error': 'Sample database not found', 'details': str(e)}
                }
        
    except ValueError as e:
        # Query validation errors
        return {
            'statusCode': 403,
            'body': {'error': str(e)}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': f'Internal error: {str(e)}'}
        }