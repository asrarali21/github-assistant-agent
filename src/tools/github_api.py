from typing import Optional

import httpx
from src.config import settings




TOKEN=settings.Settings.GITHUB_TOKEN

GITHUB_BASE_URL="https://api.github.com"


def _get_headers()->dict:
     """
    Build request headers for GitHub API calls.
    """
     headers = {
          "accept":"application/vnd.github+json"
     }
     if TOKEN:
          headers["Authorization"] = f"Bearer {TOKEN}"

     return headers

def get_open_pull_request(repo : str):
    """
    Fetches number of open PRs for a given GitHub repository.

    Example:
        repo = "vercel/next.js"
    """

    url = f"{GITHUB_BASE_URL}/repos/{repo}/pulls"
    headers = _get_headers()
    response = httpx.get(url=url , headers=headers)

    if response.status_code != 200:
         return f"⚠️ GitHub API error: {response.json().get('message')}"
    
    pr_list = response.json()

    count = len(pr_list)


    return f"There are {count} open pull requests in {repo}."
         







