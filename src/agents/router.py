from src.agents.classifier import classifier_agent , ClassificationResult
from src.tools.github_api import get_open_pull_request
from src.tools.search import web_search
from src.rag.rag_chain import get_rag_chain
from src.rag.vectorstore import ingest_repo_to_vectorstore



ingested_repos = set()

def router_agent(query:str , decision : ClassificationResult):
    print(f"Routing to {decision.action} | Context {decision.repo}")

    if decision.action == "GITHUB_API":
        return get_open_pull_request(decision.repo)
    elif decision.action == "SEARCH":
        return web_search(query=query)
    elif decision.action =="RAG":
        if decision.repo:
            # --- 2. The Smart Check ---
            if decision.repo not in ingested_repos:
                repo_url = f"https://github.com/{decision.repo}"
                print(f"🔄 New Repo detected: {decision.repo}. Ingesting...")
                ingest_repo_to_vectorstore(repo_url)
                # Mark as done!
                ingested_repos.add(decision.repo)
                print(f"✅ {decision.repo} added to memory!")
            else:
                print(f"⚡️ {decision.repo} is already ingested. Skipping download.")

        from src.rag.retriever import get_retriever
        retriever = get_retriever()
        rag_chain = get_rag_chain(retriever)
        return rag_chain.invoke(query)
    else :
        print(f"⚠️ Warning: Unknown action '{decision.action}'")
        return "I'm sorry, I wasn't sure which tool to use for that request."

def route_query(query:str):
    decision = classifier_agent.classify(query=query)
    return router_agent(query , decision)
