#!/usr/bin/env python3
"""
Local test script for the SQL query function.
Set database environment variables before running:
  export DB_HOST='your-db-host'
  export DB_PORT='25060'
  export DB_NAME='your-db-name'
  export DB_USER='your-db-user'
  export DB_PASSWORD='your-db-password'
"""

import os
import sys
import json
import importlib.util

# Load the __main__.py module
spec = importlib.util.spec_from_file_location("sql_query_module", "__main__.py")
sql_query_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sql_query_module)
main = sql_query_module.main

# Test queries
test_queries = [
    # Valid SELECT queries
    {
        'name': 'Simple SELECT',
        'event': {'query': 'SELECT 1 as test_number, NOW() as current_time'}
    },
    {
        'name': 'Table query (adjust table name as needed)',
        'event': {'query': 'SELECT * FROM pg_tables WHERE schemaname = \'public\' LIMIT 5'}
    },
    {
        'name': 'WITH clause (CTE)',
        'event': {'query': 'WITH test AS (SELECT 1 as num) SELECT * FROM test'}
    },
    # Invalid queries
    {
        'name': 'Missing query parameter',
        'event': {}
    },
    {
        'name': 'INSERT attempt (should be blocked)',
        'event': {'query': 'INSERT INTO test VALUES (1)'}
    },
    {
        'name': 'UPDATE attempt (should be blocked)',
        'event': {'query': 'UPDATE users SET name = \'test\' WHERE id = 1'}
    },
    {
        'name': 'DELETE attempt (should be blocked)',
        'event': {'query': 'DELETE FROM users WHERE id = 1'}
    },
    {
        'name': 'DROP attempt (should be blocked)',
        'event': {'query': 'DROP TABLE users'}
    },
    {
        'name': 'Invalid SQL syntax',
        'event': {'query': 'SELECT * FROM'}
    }
]

def test_sql_function():
    # Check if DATABASE_URL is set
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        print("\nExample:")
        print("  export DATABASE_URL='postgresql://user:password@host:port/dbname?sslmode=require'")
        sys.exit(1)
    
    print("Database connection configured.")
    print()
    
    for test in test_queries:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print(f"Query: {test['event'].get('query', 'No query provided')}")
        print('-'*60)
        
        try:
            result = main(test['event'], {})
            
            print(f"Status Code: {result.get('statusCode')}")
            
            body = result.get('body', {})
            if result['statusCode'] == 200:
                print(f"Columns: {body.get('columns', [])}")
                print(f"Row Count: {body.get('row_count', 0)}")
                print(f"Truncated: {body.get('truncated', False)}")
                
                # Print first few rows
                rows = body.get('rows', [])
                if rows:
                    print("\nFirst few rows:")
                    for i, row in enumerate(rows[:3]):
                        print(f"  Row {i+1}: {json.dumps(row, default=str, indent=2)}")
                    if len(rows) > 3:
                        print(f"  ... ({len(rows) - 3} more rows)")
            else:
                print(f"Error: {body.get('error')}")
                if 'details' in body:
                    print(f"Details: {body.get('details')}")
                    
        except Exception as e:
            print(f"Test failed with exception: {str(e)}")
        
        print('='*60)

if __name__ == "__main__":
    test_sql_function()