

import httpx



searxNG_url="http://localhost:8080/search"




def web_search(query:str , nums_result : int = 5)->list[dict]:
    """
    Search the web using SearxNG.

    Parameters:
        query (str): the search query
        num_results (int): how many results to return

    Returns:
        List of search results (title, url, content)
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

      
    params = {
        "q": query,
        "format": "json",
        "language": "en"
    }

    try:
      reponse = httpx.get( url=searxNG_url , headers=headers,params=params  ,timeout=10)
    except Exception as e:
       return [{"error":f"searxNG error {str(e)}"}]
    
    if reponse.status_code != 200:
       return [{"error": f"API Error {reponse.text}"}]
    

    data = reponse.json()

    results = data.get("results" , [])


    if not results:
        return "No results found."
        

    return results[:nums_result]