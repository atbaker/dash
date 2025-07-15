"""
Database utility functions for executing queries.
"""
import psycopg
from psycopg.rows import dict_row
from sql_utils import serialize_row, is_read_only_query


def execute_read_only_query(query, database_url):
    """
    Execute a read-only SQL query against the database.
    
    Args:
        query (str): The SQL query to execute
        database_url (str): PostgreSQL connection string
        
    Returns:
        dict: Result dictionary with columns, rows, row_count, and truncated flag
        
    Raises:
        ValueError: If query is not read-only
        psycopg.Error: For database-related errors
    """
    # Validate query is read-only
    if not is_read_only_query(query):
        raise ValueError("Only SELECT queries are allowed")
    
    # Connect to database
    with psycopg.connect(database_url, connect_timeout=10, row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            # Set statement timeout to 30 seconds
            cursor.execute("SET statement_timeout = '30s'")
            
            # Execute the user's query
            cursor.execute(query)
            
            # Fetch results (limit to 1000 rows for safety)
            results = cursor.fetchmany(1000)
            
            # Get column names
            columns = [desc.name for desc in cursor.description] if cursor.description else []
            
            # Check if there are more results
            has_more = len(results) == 1000
    
    # Serialize rows to ensure all values are JSON-compatible
    serialized_rows = [serialize_row(row) for row in results]
    
    response_data = {
        'columns': columns,
        'rows': serialized_rows,
        'row_count': len(results),
        'truncated': has_more
    }
    
    if has_more:
        response_data['message'] = 'Results truncated to 1000 rows'
    
    return response_data