"""
GitHub API Module - Comprehensive GitHub Data Fetching

This module provides functions to fetch various data from the GitHub API including:
- Pull request counts (with proper pagination)
- Repository statistics
- Contributors analysis
- Commit history
- Issue statistics
- Language breakdown
- Release information
"""

from typing import Optional, Dict, Any, List
import httpx
import asyncio
from src.config import settings

TOKEN = settings.Settings.GITHUB_TOKEN
GITHUB_BASE_URL = "https://api.github.com"

# Rate limit tracking
_rate_limit_remaining = None
_rate_limit_reset = None


def _get_headers() -> dict:
    """Build request headers for GitHub API calls."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def _check_rate_limit(response: httpx.Response) -> None:
    """Track rate limit from response headers."""
    global _rate_limit_remaining, _rate_limit_reset
    _rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
    _rate_limit_reset = response.headers.get("X-RateLimit-Reset")


def _format_number(num: int) -> str:
    """Format large numbers with K/M suffix for readability."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def _parse_link_header(link_header: str) -> Dict[str, str]:
    """Parse GitHub Link header for pagination info."""
    links = {}
    if not link_header:
        return links
    
    parts = link_header.split(", ")
    for part in parts:
        url_part, rel_part = part.split("; ")
        url = url_part.strip("<>")
        rel = rel_part.replace('rel="', '').replace('"', '')
        links[rel] = url
    return links




def get_open_pull_requests(repo: str) -> str:
    """
    Fetches the ACCURATE count of open PRs for a given repository.
    Uses GitHub's Search API which returns total_count for accurate results.
    
    Args:
        repo: Repository in 'owner/repo' format (e.g., 'vercel/next.js')
    
    Returns:
        Formatted string with PR count information
    """
    headers = _get_headers()
    
    # Use Search API which returns total_count accurately
    # This is more reliable than pagination for counting
    url = f"{GITHUB_BASE_URL}/search/issues"
    params = {
        "q": f"repo:{repo} is:pr is:open",
        "per_page": 1  # We only need the count, not the items
    }
    
    try:
        response = httpx.get(url, headers=headers, params=params)
        _check_rate_limit(response)
        
        if response.status_code == 422:
            return f"❌ Repository '{repo}' not found or invalid. Please check the repository name."
        if response.status_code == 403:
            return "⚠️ API rate limit exceeded. Please try again later."
        if response.status_code != 200:
            return f"⚠️ GitHub API error: {response.json().get('message', 'Unknown error')}"
        
        data = response.json()
        total_count = data.get("total_count", 0)
        
        # Also get closed PR count for context
        closed_params = {
            "q": f"repo:{repo} is:pr is:closed",
            "per_page": 1
        }
        closed_response = httpx.get(url, headers=headers, params=closed_params)
        closed_count = 0
        if closed_response.status_code == 200:
            closed_count = closed_response.json().get("total_count", 0)
        
        merged_params = {
            "q": f"repo:{repo} is:pr is:merged",
            "per_page": 1
        }
        merged_response = httpx.get(url, headers=headers, params=merged_params)
        merged_count = 0
        if merged_response.status_code == 200:
            merged_count = merged_response.json().get("total_count", 0)
        
        total_prs = total_count + closed_count
        merge_rate = (merged_count / closed_count * 100) if closed_count > 0 else 0
        
        return f"""📊 **Pull Request Stats for {repo}**

**Open PRs:** {_format_number(total_count)} ({total_count:,})
**Closed PRs:** {_format_number(closed_count)} ({closed_count:,})
**Merged PRs:** {_format_number(merged_count)} ({merged_count:,})
**Total PRs:** {_format_number(total_prs)} ({total_prs:,})

**Merge Rate:** {merge_rate:.1f}% of closed PRs were merged
"""
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"




def get_repository_stats(repo: str) -> str:
    """
    Fetches comprehensive repository statistics.
    
    Args:
        repo: Repository in 'owner/repo' format
    
    Returns:
        Formatted string with repository statistics
    """
    headers = _get_headers()
    url = f"{GITHUB_BASE_URL}/repos/{repo}"
    
    try:
        response = httpx.get(url, headers=headers)
        _check_rate_limit(response)
        
        if response.status_code == 404:
            return f"❌ Repository '{repo}' not found."
        if response.status_code != 200:
            return f"⚠️ GitHub API error: {response.json().get('message', 'Unknown error')}"
        
        data = response.json()
        
        stats = {
            "name": data.get("full_name"),
            "description": data.get("description", "No description"),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "watchers": data.get("subscribers_count", 0),
            "open_issues": data.get("open_issues_count", 0),
            "language": data.get("language", "Not specified"),
            "license": data.get("license", {}).get("name", "No license") if data.get("license") else "No license",
            "created": data.get("created_at", "")[:10],
            "updated": data.get("updated_at", "")[:10],
            "topics": data.get("topics", [])[:5],
            "default_branch": data.get("default_branch", "main"),
            "is_fork": data.get("fork", False),
            "archived": data.get("archived", False),
            "size_kb": data.get("size", 0)
        }
        
        result = f"""📊 **Repository Stats for {stats['name']}**

📝 **Description:** {stats['description']}

⭐ **Stars:** {_format_number(stats['stars'])} ({stats['stars']:,})
🍴 **Forks:** {_format_number(stats['forks'])} ({stats['forks']:,})
👀 **Watchers:** {_format_number(stats['watchers'])} ({stats['watchers']:,})
🐛 **Open Issues:** {_format_number(stats['open_issues'])} ({stats['open_issues']:,})

💻 **Language:** {stats['language']}
📜 **License:** {stats['license']}
📁 **Size:** {stats['size_kb']:,} KB
🌿 **Default Branch:** {stats['default_branch']}

📅 **Created:** {stats['created']}
🔄 **Last Updated:** {stats['updated']}
"""
        
        if stats['topics']:
            result += f"\n🏷️ **Topics:** {', '.join(stats['topics'])}"
        
        if stats['archived']:
            result += "\n\n⚠️ **Note:** This repository is archived."
        if stats['is_fork']:
            result += "\n\n🍴 **Note:** This is a forked repository."
            
        return result
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"



def get_top_contributors(repo: str, limit: int = 10) -> str:
    """
    Fetches top contributors for a repository.
    
    Args:
        repo: Repository in 'owner/repo' format
        limit: Number of top contributors to return (default 10)
    
    Returns:
        Formatted string with contributor information
    """
    headers = _get_headers()
    url = f"{GITHUB_BASE_URL}/repos/{repo}/contributors"
    params = {"per_page": min(limit, 30)}
    
    try:
        response = httpx.get(url, headers=headers, params=params)
        _check_rate_limit(response)
        
        if response.status_code == 404:
            return f"❌ Repository '{repo}' not found."
        if response.status_code != 200:
            return f"⚠️ GitHub API error: {response.json().get('message', 'Unknown error')}"
        
        contributors = response.json()[:limit]
        
        if not contributors:
            return f"📊 No contributors found for {repo}."
        
        result = f"👥 **Top {len(contributors)} Contributors for {repo}**\n\n"
        
        # Calculate total contributions for percentage
        total_contributions = sum(c.get("contributions", 0) for c in contributors)
        
        for i, contributor in enumerate(contributors, 1):
            name = contributor.get("login", "Unknown")
            contributions = contributor.get("contributions", 0)
            percentage = (contributions / total_contributions * 100) if total_contributions > 0 else 0
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            result += f"{medal} **{name}** - {contributions:,} commits ({percentage:.1f}%)\n"
        
        return result
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"




def get_recent_commits(repo: str, limit: int = 10) -> str:
    """
    Fetches recent commits from a repository.
    
    Args:
        repo: Repository in 'owner/repo' format
        limit: Number of recent commits to return (default 10)
    
    Returns:
        Formatted string with commit information
    """
    headers = _get_headers()
    url = f"{GITHUB_BASE_URL}/repos/{repo}/commits"
    params = {"per_page": min(limit, 30)}
    
    try:
        response = httpx.get(url, headers=headers, params=params)
        _check_rate_limit(response)
        
        if response.status_code == 404:
            return f"❌ Repository '{repo}' not found."
        if response.status_code != 200:
            return f"⚠️ GitHub API error: {response.json().get('message', 'Unknown error')}"
        
        commits = response.json()[:limit]
        
        if not commits:
            return f"📊 No commits found for {repo}."
        
        result = f"📝 **Recent {len(commits)} Commits in {repo}**\n\n"
        
        for commit in commits:
            sha = commit.get("sha", "")[:7]
            commit_data = commit.get("commit", {})
            message = commit_data.get("message", "No message").split("\n")[0][:60]
            author = commit_data.get("author", {}).get("name", "Unknown")
            date = commit_data.get("author", {}).get("date", "")[:10]
            
            result += f"• `{sha}` - {message}\n  👤 {author} | 📅 {date}\n\n"
        
        return result
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"


def get_issue_stats(repo: str) -> str:
    """
    Fetches issue statistics for a repository.
    
    Args:
        repo: Repository in 'owner/repo' format
    
    Returns:
        Formatted string with issue statistics
    """
    headers = _get_headers()
    
    try:
        # Get open issues count
        open_url = f"{GITHUB_BASE_URL}/repos/{repo}/issues"
        open_params = {"state": "open", "per_page": 1}
        open_response = httpx.get(open_url, headers=headers, params=open_params)
        
        if open_response.status_code == 404:
            return f"❌ Repository '{repo}' not found."
        if open_response.status_code != 200:
            return f"⚠️ GitHub API error: {open_response.json().get('message', 'Unknown error')}"
        
        # Parse open issues count from Link header
        open_link = open_response.headers.get("Link", "")
        open_links = _parse_link_header(open_link)
        
        if "last" in open_links:
            import re
            match = re.search(r'page=(\d+)', open_links["last"])
            open_count = int(match.group(1)) if match else len(open_response.json())
        else:
            open_count = len(open_response.json())
        
        # Get closed issues count
        closed_params = {"state": "closed", "per_page": 1}
        closed_response = httpx.get(open_url, headers=headers, params=closed_params)
        
        closed_link = closed_response.headers.get("Link", "")
        closed_links = _parse_link_header(closed_link)
        
        if "last" in closed_links:
            import re
            match = re.search(r'page=(\d+)', closed_links["last"])
            closed_count = int(match.group(1)) if match else len(closed_response.json())
        else:
            closed_count = len(closed_response.json())
        
        total = open_count + closed_count
        close_rate = (closed_count / total * 100) if total > 0 else 0
        
        result = f"""🐛 **Issue Statistics for {repo}**

📊 **Overview:**
• **Open Issues:** {open_count:,}
• **Closed Issues:** {closed_count:,}
• **Total Issues:** {total:,}

✅ **Close Rate:** {close_rate:.1f}%
"""
        
        return result
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"



def get_language_breakdown(repo: str) -> str:
    """
    Fetches programming language breakdown for a repository.
    
    Args:
        repo: Repository in 'owner/repo' format
    
    Returns:
        Formatted string with language breakdown
    """
    headers = _get_headers()
    url = f"{GITHUB_BASE_URL}/repos/{repo}/languages"
    
    try:
        response = httpx.get(url, headers=headers)
        _check_rate_limit(response)
        
        if response.status_code == 404:
            return f"❌ Repository '{repo}' not found."
        if response.status_code != 200:
            return f"⚠️ GitHub API error: {response.json().get('message', 'Unknown error')}"
        
        languages = response.json()
        
        if not languages:
            return f"📊 No language data available for {repo}."
        
        total_bytes = sum(languages.values())
        
        result = f"💻 **Language Breakdown for {repo}**\n\n"
        
        # Sort by bytes and show percentages
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        
        for lang, bytes_count in sorted_langs:
            percentage = (bytes_count / total_bytes * 100)
            bar_length = int(percentage / 5)  # Scale to 20 chars max
            bar = "█" * bar_length + "░" * (20 - bar_length)
            result += f"**{lang}**\n{bar} {percentage:.1f}%\n\n"
        
        return result
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"



def get_latest_release(repo: str) -> str:
    """
    Fetches the latest release information for a repository.
    
    Args:
        repo: Repository in 'owner/repo' format
    
    Returns:
        Formatted string with release information
    """
    headers = _get_headers()
    url = f"{GITHUB_BASE_URL}/repos/{repo}/releases/latest"
    
    try:
        response = httpx.get(url, headers=headers)
        _check_rate_limit(response)
        
        if response.status_code == 404:
            releases_url = f"{GITHUB_BASE_URL}/repos/{repo}/releases"
            releases_response = httpx.get(releases_url, headers=headers, params={"per_page": 1})
            
            if releases_response.status_code == 404:
                return f"❌ Repository '{repo}' not found."
            
            releases = releases_response.json()
            if not releases:
                return f"📦 No releases found for {repo}. The repository may use tags instead."
            
            data = releases[0]
        elif response.status_code != 200:
            return f"⚠️ GitHub API error: {response.json().get('message', 'Unknown error')}"
        else:
            data = response.json()
        
        name = data.get("name") or data.get("tag_name", "Unnamed")
        tag = data.get("tag_name", "No tag")
        published = data.get("published_at", "")[:10]
        author = data.get("author", {}).get("login", "Unknown")
        prerelease = data.get("prerelease", False)
        body = data.get("body", "No release notes")[:300]
        
        assets = data.get("assets", [])
        total_downloads = sum(a.get("download_count", 0) for a in assets)
        
        result = f"""📦 **Latest Release for {repo}**

🏷️ **{name}** (`{tag}`)
{'⚠️ Pre-release' if prerelease else '✅ Stable Release'}

📅 **Published:** {published}
👤 **Author:** {author}
📥 **Total Downloads:** {total_downloads:,}
📎 **Assets:** {len(assets)} files

📝 **Release Notes:**
{body}{'...' if len(data.get('body', '')) > 300 else ''}
"""
        
        return result
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"



def get_repo_overview(repo: str) -> str:
    """
    Fetches a comprehensive overview of a repository.
    Combines stats, latest release, and top contributor.
    
    Args:
        repo: Repository in 'owner/repo' format
    
    Returns:
        Formatted string with comprehensive repository overview
    """
    headers = _get_headers()
    
    try:
        repo_url = f"{GITHUB_BASE_URL}/repos/{repo}"
        repo_response = httpx.get(repo_url, headers=headers)
        
        if repo_response.status_code == 404:
            return f"❌ Repository '{repo}' not found."
        if repo_response.status_code != 200:
            return f"⚠️ GitHub API error: {repo_response.json().get('message', 'Unknown error')}"
        
        repo_data = repo_response.json()
        
        # Get top contributor
        contrib_url = f"{GITHUB_BASE_URL}/repos/{repo}/contributors"
        contrib_response = httpx.get(contrib_url, headers=headers, params={"per_page": 1})
        top_contributor = "N/A"
        if contrib_response.status_code == 200 and contrib_response.json():
            top_contributor = contrib_response.json()[0].get("login", "Unknown")
        
        # Get languages
        lang_url = f"{GITHUB_BASE_URL}/repos/{repo}/languages"
        lang_response = httpx.get(lang_url, headers=headers)
        top_languages = []
        if lang_response.status_code == 200 and lang_response.json():
            langs = lang_response.json()
            total = sum(langs.values())
            top_languages = [(k, v/total*100) for k, v in sorted(langs.items(), key=lambda x: x[1], reverse=True)[:3]]
        
        result = f"""🚀 **Repository Overview: {repo_data.get('full_name')}**

📝 {repo_data.get('description', 'No description')}

**📊 Key Metrics:**
• ⭐ Stars: {_format_number(repo_data.get('stargazers_count', 0))}
• 🍴 Forks: {_format_number(repo_data.get('forks_count', 0))}
• 👀 Watchers: {_format_number(repo_data.get('subscribers_count', 0))}
• 🐛 Open Issues: {_format_number(repo_data.get('open_issues_count', 0))}

**👤 Top Contributor:** {top_contributor}
"""
        
        if top_languages:
            lang_str = ", ".join([f"{lang} ({pct:.0f}%)" for lang, pct in top_languages])
            result += f"\n**💻 Top Languages:** {lang_str}"
        
        if repo_data.get('topics'):
            result += f"\n\n**🏷️ Topics:** {', '.join(repo_data['topics'][:5])}"
        
        result += f"\n\n🔗 **URL:** https://github.com/{repo}"
        
        return result
        
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}"


def get_open_pull_request(repo: str) -> str:
    """Backward compatible wrapper for get_open_pull_requests."""
    return get_open_pull_requests(repo)
