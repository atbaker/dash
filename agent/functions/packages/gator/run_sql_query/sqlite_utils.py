"""
SQLite utility functions for executing queries against sample data.
"""
import sqlite3
import os
from typing import Dict, List, Any
from sql_utils import serialize_row, is_read_only_query


def get_sqlite_db_path() -> str:
    """Get the path to the SQLite database file."""
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'gator_sample.db')


def execute_read_only_query_sqlite(query: str) -> Dict[str, Any]:
    """
    Execute a read-only SQL query against the SQLite sample database.
    
    Args:
        query (str): The SQL query to execute
        
    Returns:
        dict: Result dictionary with columns, rows, row_count, and truncated flag
        
    Raises:
        ValueError: If query is not read-only
        sqlite3.Error: For database-related errors
    """
    # Validate query is read-only
    if not is_read_only_query(query):
        raise ValueError("Only SELECT queries are allowed")
    
    db_path = get_sqlite_db_path()
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"SQLite database not found at {db_path}")
    
    # Connect to SQLite database
    with sqlite3.connect(db_path, timeout=30.0) as conn:
        # Set row factory to return dictionaries
        conn.row_factory = sqlite3.Row
        
        cursor = conn.cursor()
        
        # Execute the user's query
        cursor.execute(query)
        
        # Fetch results (limit to 1000 rows for safety)
        results = cursor.fetchmany(1000)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        
        # Check if there are more results
        has_more = len(results) == 1000
    
    # Convert sqlite3.Row objects to dictionaries and serialize
    serialized_rows = []
    for row in results:
        row_dict = dict(row)
        serialized_row = serialize_row(row_dict)
        serialized_rows.append(serialized_row)
    
    response_data = {
        'columns': columns,
        'rows': serialized_rows,
        'row_count': len(results),
        'truncated': has_more,
        'data_source': 'sqlite_sample'
    }
    
    if has_more:
        response_data['message'] = 'Results truncated to 1000 rows'
    
    return response_data


def get_database_info() -> Dict[str, Any]:
    """Get information about the SQLite sample database."""
    db_path = get_sqlite_db_path()
    
    if not os.path.exists(db_path):
        return {'error': 'SQLite database not found'}
    
    try:
        with sqlite3.connect(db_path, timeout=10.0) as conn:
            cursor = conn.cursor()
            
            # Get table information
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            table_info = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                table_info[table] = count
            
            return {
                'database_type': 'sqlite',
                'database_path': db_path,
                'tables': table_info,
                'total_rows': sum(table_info.values())
            }
    
    except sqlite3.Error as e:
        return {'error': f'Database error: {str(e)}'}