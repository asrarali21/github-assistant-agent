import os
import httpx
from typing import List, Dict, Union

# Multiple SearXNG instances as fallback
SEARXNG_INSTANCES = [
    "https://search.rhscz.eu",
    "https://searx.be",
    "https://search.sapti.me",
    "https://searx.tiekoetter.com"
]

def web_search(query: str, num_results: int = 5) -> Union[List[Dict], str]:
    """
    Search the web using SearxNG with multiple fallback instances.

    Parameters:
        query (str): the search query
        num_results (int): how many results to return

    Returns:
        List of search results (title, url, content)
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    params = {
        "q": query,
        "format": "json",
        "language": "en"
    }

    # Try each instance until one works
    for instance_url in SEARXNG_INSTANCES:
        try:
            # Remove trailing slash and add /search endpoint
            base_url = instance_url.rstrip('/')
            search_url = f"{base_url}/search"
            
            print(f"🔍 Trying search instance: {search_url}")
            
            response = httpx.get(
                url=search_url, 
                headers=headers, 
                params=params, 
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                print(f"⚠️ No results from {instance_url}, trying next...")
                continue
            
            # Format results
            formatted_results = []
            for result in results[:num_results]:
                formatted_results.append({
                    "title": result.get("title", "No title"),
                    "url": result.get("url", ""),
                    "content": result.get("content", "No description")
                })
            
            print(f"✅ Successfully got {len(formatted_results)} results from {instance_url}")
            return formatted_results
            
        except httpx.TimeoutException:
            print(f"⏱️ Timeout for {instance_url}, trying next...")
            continue
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP Error {e.response.status_code} for {instance_url}, trying next...")
            continue
        except Exception as e:
            print(f"❌ Error with {instance_url}: {str(e)}, trying next...")
            continue
    
    # If all instances fail
    error_msg = "All SearxNG instances failed. Please try again later."
    print(f"❌ {error_msg}")
    return [{"error": error_msg}] 