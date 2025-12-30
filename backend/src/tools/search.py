import httpx
from typing import List, Dict
from duckduckgo_search import DDGS

def web_search(query: str, num_results: int = 5) -> List[Dict]:
    """
    Search the web using DuckDuckGo.

    Parameters:
        query (str): the search query
        num_results (int): how many results to return

    Returns:
        List of search results (title, url, content)
    """
    try:
        print(f"🔍 Searching DuckDuckGo for: {query}")
        
        # Use DuckDuckGo search
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
        
        if not results:
            return [{"message": "No results found"}]
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", "No title"),
                "url": result.get("href", result.get("link", "")),
                "content": result.get("body", result.get("snippet", "No description"))
            })
        
        print(f"✅ Found {len(formatted_results)} results")
        return formatted_results
        
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
        return [{"error": f"Search failed: {str(e)}"}]