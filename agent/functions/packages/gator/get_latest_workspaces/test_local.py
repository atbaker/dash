#!/usr/bin/env python3
"""
Test script for get_latest_workspaces function
"""
import os
import json
from get_latest_workspaces import get_latest_workspaces

def test_function():
    """Test the get_latest_workspaces function locally"""
    
    # Check environment variables
    functions_base_url = os.environ.get('DO_FUNCTIONS_BASE_URL')
    if not functions_base_url:
        print("ERROR: DO_FUNCTIONS_BASE_URL environment variable not set")
        return
    
    print(f"Testing with base URL: {functions_base_url}")
    
    try:
        # Call the function
        result = get_latest_workspaces(functions_base_url)
        
        # Print results
        print("SUCCESS!")
        print(f"Query description: {result.get('query_description', 'N/A')}")
        print(f"Total count: {result.get('total_count', 0)}")
        print(f"Columns: {result.get('columns', [])}")
        
        workspaces = result.get('workspaces', [])
        print(f"\nFound {len(workspaces)} workspaces:")
        for i, workspace in enumerate(workspaces[:3], 1):  # Show first 3
            print(f"  {i}. {workspace.get('name', 'N/A')} - {workspace.get('domain', 'N/A')} - {workspace.get('install_date', 'N/A')}")
        
        if len(workspaces) > 3:
            print(f"  ... and {len(workspaces) - 3} more")
            
    except Exception as e:
        print(f"ERROR: {e}")
        
        # Let's also try to call run_sql_query directly to debug
        print("\nTrying to call run_sql_query directly...")
        try:
            import requests
            
            test_query = "SELECT COUNT(*) as total FROM workspaces_workspace WHERE uninstalled = FALSE"
            response = requests.post(
                f"{functions_base_url}/run_sql_query",
                json={"query": test_query},
                timeout=30
            )
            
            print(f"Direct call status code: {response.status_code}")
            print(f"Direct call response: {response.text}")
            
        except Exception as direct_error:
            print(f"Direct call also failed: {direct_error}")

if __name__ == "__main__":
    test_function()