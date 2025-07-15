# Web Search Function

## Function Instructions

This function performs web searches using the Brave Search API to find current information and news on the internet. Use this function when users ask about:

- Current events and breaking news
- Recent developments in technology, business, or industry
- Real-time information not available in the database
- Competitor analysis and market research
- Trends and public information about topics
- External context to supplement business data analysis

The function returns both web results and news articles, providing comprehensive coverage of search topics. Results include titles, URLs, descriptions, and publication dates to help provide accurate and timely information.

Use this tool when the user needs information that goes beyond their internal business data or when current/external context would enhance their understanding of business trends and market conditions.

## Input Schema (OpenAPI)

```json
{
  "parameters": [
    {
      "in": "query",
      "name": "query",
      "schema": {
        "type": "string"
      },
      "required": true,
      "description": "The search query to execute on the web"
    }
  ]
}
```

## Output Schema (OpenAPI)

```json
{
  "properties": [
    {
      "name": "query",
      "type": "string",
      "description": "The original search query"
    },
    {
      "name": "results",
      "type": "array",
      "description": "Array of search results with title, url, description, published date, and type (web or news)"
    },
    {
      "name": "result_count",
      "type": "number",
      "description": "Total number of results returned"
    },
    {
      "name": "web_count",
      "type": "number",
      "description": "Number of web search results"
    },
    {
      "name": "news_count",
      "type": "number",
      "description": "Number of news results"
    }
  ]
}
```

## Environment Variables

- `BRAVE_API_KEY`: API key from Brave Search API dashboard

## Testing

```bash
cd functions/packages/gator/web_search
pip install requests
export BRAVE_API_KEY='your_brave_api_key_here'
python test_local.py
```

## API Details

- Endpoint: `https://api.search.brave.com/res/v1/web/search`
- Returns up to 10 web results plus news results
- Includes safesearch filtering
- 10-second timeout for requests