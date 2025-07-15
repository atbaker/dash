"""
Shared web search functionality using Brave Search API.
Works with both Pipecat voice agent and DigitalOcean Functions.
"""
import os
import requests
from typing import Dict, Any, Optional


def search_web(query: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform web search using Brave Search API.
    
    Args:
        query: Search query string
        api_key: Brave API key (optional, will use environment variable if not provided)
    
    Returns:
        Dictionary containing search results or error information
    """
    try:
        if not query or not query.strip():
            return {'error': 'Query parameter is required'}
        
        # Get API key from parameter or environment variable
        if not api_key:
            api_key = os.environ.get('BRAVE_API_KEY')
        
        if not api_key:
            return {'error': 'Brave API key not configured'}
        
        # Set up request parameters
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Subscription-Token': api_key
        }
        params = {
            'q': query,
            'count': 10,  # Number of results to return (max 20)
            'search_lang': 'en',
            'country': 'US',
            'safesearch': 'moderate'
        }
        
        # Make API request
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            return {
                'error': f'Brave API error: {response.status_code}',
                'details': response.text
            }
        
        data = response.json()
        
        # Extract relevant information from response
        results = []
        web_results = data.get('web', {}).get('results', [])
        
        for result in web_results:
            results.append({
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'description': result.get('description', ''),
                'published': result.get('published', ''),
                'type': result.get('type', 'web')
            })
        
        # Include news results if available
        news_results = data.get('news', {}).get('results', [])
        for result in news_results:
            results.append({
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'description': result.get('description', ''),
                'published': result.get('published', ''),
                'type': 'news'
            })
        
        # Format response
        search_info = {
            'query': query,
            'results': results,
            'result_count': len(results),
            'web_count': len(web_results),
            'news_count': len(news_results)
        }
        
        return search_info
        
    except requests.exceptions.Timeout:
        return {'error': 'Search request timed out'}
    except requests.exceptions.RequestException as e:
        return {'error': 'Network error', 'details': str(e)}
    except Exception as e:
        return {'error': f'Internal error: {str(e)}'}



