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
    # Valid SELECT queries for Gator tables
    {
        'name': 'Count workspaces',
        'event': {'query': 'SELECT COUNT(*) as workspace_count FROM workspaces_workspace'}
    },
    {
        'name': 'Count users',
        'event': {'query': 'SELECT COUNT(*) as user_count FROM workspaces_gatoruser'}
    },
    {
        'name': 'Count messages',
        'event': {'query': 'SELECT COUNT(*) as message_count FROM later_messages_message'}
    },
    {
        'name': 'Sample workspace data',
        'event': {'query': 'SELECT name, enterprise_name, created FROM workspaces_workspace LIMIT 5'}
    },
    {
        'name': 'Messages by status',
        'event': {'query': 'SELECT status, COUNT(*) as count FROM later_messages_message GROUP BY status ORDER BY count DESC'}
    },
    {
        'name': 'Workspaces by year',
        'event': {'query': 'SELECT strftime("%Y", created) as year, COUNT(*) as count FROM workspaces_workspace GROUP BY year ORDER BY year'}
    },
    {
        'name': 'JOIN query',
        'event': {'query': 'SELECT w.name, COUNT(u.id) as user_count FROM workspaces_workspace w LEFT JOIN workspaces_gatoruser u ON w.id = u.workspace_id GROUP BY w.id, w.name ORDER BY user_count DESC LIMIT 10'}
    },
    {
        'name': 'WITH clause (CTE)',
        'event': {'query': 'WITH recent_workspaces AS (SELECT * FROM workspaces_workspace WHERE created > "2023-01-01") SELECT COUNT(*) as recent_count FROM recent_workspaces'}
    },
    # Invalid queries
    {
        'name': 'Missing query parameter',
        'event': {}
    },
    {
        'name': 'INSERT attempt (should be blocked)',
        'event': {'query': 'INSERT INTO workspaces_workspace VALUES (1)'}
    },
    {
        'name': 'UPDATE attempt (should be blocked)',
        'event': {'query': 'UPDATE workspaces_workspace SET name = "test" WHERE id = 1'}
    },
    {
        'name': 'DELETE attempt (should be blocked)',
        'event': {'query': 'DELETE FROM workspaces_workspace WHERE id = 1'}
    },
    {
        'name': 'DROP attempt (should be blocked)',
        'event': {'query': 'DROP TABLE workspaces_workspace'}
    }
]

def test_sql_function():
    # Check if DATABASE_URL is set
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and database_url != 'use-gator-sample-data':
        print("Using PostgreSQL production database.")
    else:
        print("Using SQLite sample data fallback.")
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