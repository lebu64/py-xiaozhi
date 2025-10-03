# Search Tools

Search Tools is an intelligent web search MCP toolset that provides web search, content acquisition, result caching, and other functions to help users quickly obtain internet information.

### Common Usage Scenarios

**Daily Information Search:**
- "Search for today's weather"
- "Query the distance from Beijing to Shanghai"
- "Find the latest news"
- "Search for the latest developments in artificial intelligence"

**Learning and Research:**
- "Search for information about quantum computing"
- "Look up basic concepts of machine learning"
- "Find some Python programming tutorials"
- "Search for what happened today in history"

**Shopping and Price Comparison:**
- "Search for iPhone 15 prices"
- "Query laptop recommendations"
- "Find some cost-effective phones"
- "Search for the latest promotional activities"

**Life Services:**
- "Search for nearby restaurants"
- "Query train ticket booking information"
- "Find renovation companies"
- "Search for weekend activity recommendations"

**Technical Problems:**
- "Search for Python error solutions"
- "Query API interface documentation"
- "Find software installation tutorials"
- "Search for code examples"

### Usage Tips

1. **Clear Search Intent**: Clearly describe what you want to search for
2. **Use Keywords**: Provide accurate keywords to get better results
3. **Specify Quantity**: Can request specific number of search results
4. **In-depth Understanding**: Can request detailed content of specific web pages
5. **Multiple Searches**: Can perform further searches based on search results

AI assistant will automatically call search tools based on your needs, providing accurate internet information.

## Feature Overview

### Web Search Functionality
- **Bing Search**: Intelligent search based on Bing search engine
- **Multi-language Support**: Supports Chinese, English and other language searches
- **Region Settings**: Supports search results from different regions
- **Result Quantity Control**: Can set the number of returned results

### Content Acquisition Functionality
- **Webpage Content Crawling**: Get detailed content of search result pages
- **Content Length Control**: Can limit the length of acquired content
- **Intelligent Extraction**: Automatically extracts main content of web pages
- **Formatted Output**: Returns content in easy-to-read format

### Cache Management Functionality
- **Search Result Caching**: Automatically caches search results
- **Session Management**: Supports multiple search sessions
- **Cache Query**: Can view historical search results
- **Cache Cleanup**: Supports clearing search cache

### Session Management Functionality
- **Session Tracking**: Tracks search session status
- **Session Information**: Provides detailed session information
- **Session Switching**: Supports switching between multiple search sessions
- **Session Persistence**: Saves search session data

## Tool List

### 1. Search Tools

#### search_bing - Bing Search
Execute Bing search to obtain web information.

**Parameters:**
- `query` (required): Search keywords
- `num_results` (optional): Number of returned results, default 5, maximum 10
- `language` (optional): Search language, default "zh-cn"
- `region` (optional): Search region, default "CN"

**Usage Scenarios:**
- Daily information search
- Learning and research
- News queries
- Technical problem solving

### 2. Content Acquisition Tools

#### fetch_webpage_content - Get Webpage Content
Get detailed content of specified search result web pages.

**Parameters:**
- `result_id` (required): Search result ID
- `max_length` (optional): Maximum content length, default 8000, maximum 20000

**Usage Scenarios:**
- In-depth reading of webpage content
- Getting article details
- Analyzing webpage information
- Content research

### 3. Cache Management Tools

#### get_search_results - Get Search Result Cache
Get cached search results.

**Parameters:**
- `session_id` (optional): Session ID

**Usage Scenarios:**
- View historical search results
- Review search records
- Session management
- Result comparison

#### clear_search_cache - Clear Search Cache
Clear all search cache data.

**Parameters:**
None

**Usage Scenarios:**
- Clean up search records
- Reset search status
- Free up memory space
- Privacy protection

### 4. Session Management Tools

#### get_session_info - Get Session Information
Get detailed information of current search session.

**Parameters:**
None

**Usage Scenarios:**
- View session status
- Session statistics
- System monitoring
- Debugging information

## Usage Examples

### Basic Search Examples

```python
# Basic search
result = await mcp_server.call_tool("search_bing", {
    "query": "Latest developments in artificial intelligence",
    "num_results": 5
})

# Search with specified language and region
result = await mcp_server.call_tool("search_bing", {
    "query": "artificial intelligence",
    "num_results": 10,
    "language": "en-us",
    "region": "US"
})

# Get webpage content
result = await mcp_server.call_tool("fetch_webpage_content", {
    "result_id": "search_result_123",
    "max_length": 10000
})
```

### Cache Management Examples

```python
# Get search result cache
result = await mcp_server.call_tool("get_search_results", {})

# Get search results for specific session
result = await mcp_server.call_tool("get_search_results", {
    "session_id": "session_123"
})

# Clear search cache
result = await mcp_server.call_tool("clear_search_cache", {})
```

### Session Management Examples

```python
# Get session information
result = await mcp_server.call_tool("get_session_info", {})
```

## Data Structures

### Search Result (SearchResult)
```python
{
    "id": "search_result_123",
    "title": "Latest Development Trends in Artificial Intelligence",
    "url": "https://example.com/ai-trends",
    "snippet": "Artificial intelligence technology achieved major breakthroughs in 2025...",
    "source": "example.com",
    "has_content": true,
    "created_at": "2025-01-15T10:30:00Z"
}
```

### Search Response (SearchResponse)
```python
{
    "success": true,
    "query": "Latest developments in artificial intelligence",
    "num_results": 5,
    "results": [
        {
            "id": "search_result_123",
            "title": "Latest Development Trends in Artificial Intelligence",
            "url": "https://example.com/ai-trends",
            "snippet": "Artificial intelligence technology achieved major breakthroughs in 2025...",
            "source": "example.com"
        }
    ],
    "session_info": {
        "session_id": "session_123",
        "created_at": "2025-01-15T10:25:00Z",
        "total_searches": 1,
        "total_results": 5
    }
}
```

### Webpage Content (WebpageContent)
```python
{
    "success": true,
    "result_id": "search_result_123",
    "result_info": {
        "id": "search_result_123",
        "title": "Latest Development Trends in Artificial Intelligence",
        "url": "https://example.com/ai-trends",
        "snippet": "Artificial intelligence technology achieved major breakthroughs in 2025...",
        "source": "example.com"
    },
    "content": "Artificial intelligence technology achieved major breakthroughs in 2025, including large language models, computer vision, natural language processing and other fields...",
    "content_length": 5420
}
```

### Session Information (SessionInfo)
```python
{
    "session_id": "session_123",
    "created_at": "2025-01-15T10:25:00Z",
    "last_search_at": "2025-01-15T10:30:00Z",
    "total_searches": 3,
    "total_results": 15,
    "cached_results": 12,
    "status": "active"
}
```

## Search Techniques

### 1. Keyword Selection
- Use specific, accurate keywords
- Avoid overly broad search terms
- Can use multiple keyword combinations
- Try different expression methods

### 2. Language and Region Settings
- Chinese search: language="zh-cn", region="CN"
- English search: language="en-us", region="US"
- Choose appropriate language based on content source
- Region settings affect search result relevance

### 3. Result Quantity Control
- General search: 5-10 results
- In-depth research: 10 results
- Quick browsing: 3-5 results
- Avoid getting too many results at once

### 4. Content Acquisition Strategy
- First search to get result list
- Select highly relevant results to get content
- Adjust content length as needed
- Can get content from multiple results for comparison

## Best Practices

### 1. Search Strategy
- From broad to specific, gradually refine search
- Use multiple keyword combinations
- Try different search angles
- Pay attention to timeliness of search results

### 2. Content Processing
- Get detailed webpage content as needed
- Reasonably set content length limits
- Pay attention to content source and reliability
- Can get content from multiple sources for comparison

### 3. Cache Utilization
- Make full use of search result cache
- Regularly clean up unnecessary cache
- Use session management functions
- Pay attention to cache validity

### 4. Privacy Protection
- Clean cache promptly after sensitive searches
- Pay attention to privacy of search content
- Reasonably use session management functions
- Avoid searching for sensitive information

## Supported Search Types

### Information Search
- News and information
- Academic materials
- Encyclopedia knowledge
- Technical documentation

### Commercial Search
- Product information
- Price comparison
- Business information
- Market analysis

### Life Services
- Local services
- Dining and entertainment
- Transportation
- Life guides

### Technical Support
- Programming problems
- Software usage
- Error resolution
- Technical tutorials

## Precautions

1. **Network Dependency**: Search functionality requires stable network connection
2. **Search Limitations**: Comply with search engine usage specifications
3. **Content Accuracy**: Search result accuracy depends on original sources
4. **Copyright Issues**: Pay attention to copyright and usage restrictions of search content
5. **Privacy Protection**: Pay attention to privacy of search content

## Troubleshooting

### Common Issues
1. **No Search Results**: Try different keyword combinations
2. **Webpage Content Acquisition Failure**: Check network connection and target website status
3. **Slow Search Speed**: Reduce number of search results or content length
4. **Cache Issues**: Clear search cache and search again

### Debugging Methods
1. Check if search keywords are correct
2. Verify network connection status
3. View session information to understand search status
4. Use cache management functions to troubleshoot problems

### Performance Optimization
1. Reasonably set number of search results
2. Get webpage content as needed
3. Regularly clean search cache
4. Use session management to optimize search process

With Search Tools, you can quickly obtain various information from the internet, supporting various needs for learning, work, and life.
