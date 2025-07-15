#!/usr/bin/env python3
"""
Local test script for the web search function.
Set BRAVE_API_KEY environment variable before running:
  export BRAVE_API_KEY='your_brave_api_key_here'
"""

import os
import sys
import json
import importlib.util

# Load the __main__.py module
spec = importlib.util.spec_from_file_location("web_search_module", "__main__.py")
web_search_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_search_module)
main = web_search_module.main

# Test queries
test_searches = [
    # Valid search queries
    {
        'name': 'Technology search',
        'event': {'query': 'artificial intelligence latest news'}
    },
    {
        'name': 'Business search',
        'event': {'query': 'DigitalOcean GenAI platform'}
    },
    {
        'name': 'Current events',
        'event': {'query': 'tech industry trends 2024'}
    },
    {
        'name': 'Specific company search',
        'event': {'query': 'Slack productivity features'}
    },
    {
        'name': 'Market research',
        'event': {'query': 'SaaS business metrics'}
    },
    # Edge cases
    {
        'name': 'Missing query parameter',
        'event': {}
    },
    {
        'name': 'Empty query',
        'event': {'query': ''}
    },
    {
        'name': 'Very short query',
        'event': {'query': 'AI'}
    },
    {
        'name': 'Long complex query',
        'event': {'query': 'how to build scalable artificial intelligence applications using cloud infrastructure and modern development practices'}
    }
]

def test_web_search_function():
    # Check if BRAVE_API_KEY is set
    api_key = os.environ.get('BRAVE_API_KEY')
    
    if not api_key:
        print("ERROR: BRAVE_API_KEY environment variable not set")
        print("\nExample:")
        print("  export BRAVE_API_KEY='your_brave_api_key_here'")
        print("\nGet your API key from: https://api-dashboard.search.brave.com/")
        sys.exit(1)
    
    print("Brave API key configured.")
    print()
    
    for test in test_searches:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print(f"Query: {test['event'].get('query', 'No query provided')}")
        print('-'*60)
        
        try:
            result = main(test['event'], {})
            
            print(f"Status Code: {result.get('statusCode')}")
            
            body = result.get('body', {})
            if result['statusCode'] == 200:
                print(f"Search Query: {body.get('query', '')}")
                print(f"Total Results: {body.get('result_count', 0)}")
                print(f"Web Results: {body.get('web_count', 0)}")
                print(f"News Results: {body.get('news_count', 0)}")
                
                # Print first few results
                results = body.get('results', [])
                if results:
                    print("\nFirst few results:")
                    for i, result_item in enumerate(results[:3]):
                        print(f"\n  Result {i+1}:")
                        print(f"    Title: {result_item.get('title', 'N/A')}")
                        print(f"    URL: {result_item.get('url', 'N/A')}")
                        print(f"    Type: {result_item.get('type', 'N/A')}")
                        print(f"    Description: {result_item.get('description', 'N/A')[:100]}{'...' if len(result_item.get('description', '')) > 100 else ''}")
                        if result_item.get('published'):
                            print(f"    Published: {result_item.get('published')}")
                    
                    if len(results) > 3:
                        print(f"\n  ... ({len(results) - 3} more results)")
                else:
                    print("\nNo results found.")
            else:
                print(f"Error: {body.get('error')}")
                if 'details' in body:
                    print(f"Details: {body.get('details')}")
                    
        except Exception as e:
            print(f"Test failed with exception: {str(e)}")
        
        print('='*60)

if __name__ == "__main__":
    test_web_search_function()