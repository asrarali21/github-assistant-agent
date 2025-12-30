# from src.agents.classifier import classifier_agent , ClassificationResult
# from src.tools.github_api import get_open_pull_request
# from src.tools.search import web_search
# from src.rag.vectorstore import ingest_repo_to_vectorstore
# from src.rag.rag_chain import get_rag_chain

# ingested_repo=set()
# def router_agent(query , decision:ClassificationResult):

#     print(f"routing{decision.action} , repo {decision.repo}" )

#     if(decision.action == "GITHUB_API"):
#         return get_open_pull_request(decision.repo)
#     elif(decision.action =="SEARCH"):
#         return web_search(query=query)
#     elif(decision.action == "RAG"):
#          if decision.repo not in ingested_repo:
#              repo_url=f"https://github.com/{decision.repo}"
#              print(f"New repo Detected{repo_url}")
#              ingest_repo_to_vectorstore(repo_url)
#              ingested_repo.add(decision.repo)
#              print(f"{decision.repo} added to memory!")
#          else:
#             print(f" {decision.repo} is already ingested. Skipping download.")
#             from src.rag.retriever import get_retriever
#             retriver = get_retriever
#             rag_chain = get_rag_chain(retriver)
#             return rag_chain.invoke(query)
#     else :
#         print(f" Warning: Unknown action '{decision.action}'")
#         return "I'm sorry, I wasn't sure which tool to use for that request."


# def router_query(query:str):
#     decision = classifier_agent.classify(  query=query)
#     return router_agent(query=query , decision=decision)



from src.agents.classifier import classifier_agent , ClassificationResult
from src.tools.github_api import (
    get_open_pull_requests,
    get_repository_stats,
    get_top_contributors,
    get_recent_commits,
    get_issue_stats,
    get_language_breakdown,
    get_latest_release,
    get_repo_overview
)
from src.tools.search import web_search
from src.rag.rag_chain import get_rag_chain
from src.rag.vectorstore import ingest_repo_to_vectorstore



ingested_repos = set()

# Map action types to their corresponding functions
GITHUB_ACTION_MAP = {
    "GITHUB_PR_COUNT": get_open_pull_requests,
    "GITHUB_STATS": get_repository_stats,
    "GITHUB_CONTRIBUTORS": get_top_contributors,
    "GITHUB_COMMITS": get_recent_commits,
    "GITHUB_ISSUES": get_issue_stats,
    "GITHUB_LANGUAGES": get_language_breakdown,
    "GITHUB_RELEASES": get_latest_release,
    "GITHUB_OVERVIEW": get_repo_overview,
}

def router_agent(query:str , decision : ClassificationResult):
    print(f"🔀 Routing to {decision.action} | Repo: {decision.repo}")
    print(f"   Reason: {decision.reason}")

    # Handle GitHub API actions
    if decision.action in GITHUB_ACTION_MAP:
        if not decision.repo:
            return "❌ I need a repository name to fetch GitHub data. Please specify in 'owner/repo' format."
        
        handler = GITHUB_ACTION_MAP[decision.action]
        return handler(decision.repo)
    
    # Handle web search
    elif decision.action == "SEARCH":
        return web_search(query=query)
    
    # Handle RAG for code understanding
    elif decision.action =="RAG":
        if decision.repo:
            # --- Smart ingestion check ---
            if decision.repo not in ingested_repos:
                repo_url = f"https://github.com/{decision.repo}"
                print(f"📥 New Repo detected: {decision.repo}. Ingesting...")
                ingest_repo_to_vectorstore(repo_url)
                # Mark as done!
                ingested_repos.add(decision.repo)
                print(f"✅ {decision.repo} added to memory!")
            else:
                print(f"📦 {decision.repo} is already ingested. Skipping download.")

        from src.rag.retriever import get_retriever
        retriever = get_retriever()
        rag_chain = get_rag_chain(retriever)
        return rag_chain.invoke(query)
    
    else:
        print(f"⚠️ Warning: Unknown action '{decision.action}'")
        return "I'm sorry, I wasn't sure which tool to use for that request."

def route_query(query:str):
    decision = classifier_agent.classify(query=query)
    return router_agent(query , decision)