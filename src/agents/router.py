from src.agents.classifier import classifier_agent , ClassificationResult
from src.tools.github_api import get_open_pull_request
from src.tools.search import web_search
from src.rag.rag_chain import get_rag_chain

def router_agent(query:str , decision : ClassificationResult):
    print(f"Routing to {decision.action} | Context {decision.repo}")

    if decision.action == "GITHUB_API":
        print(get_open_pull_request(decision.repo))
    elif decision.action == "SEARCH":
        print( web_search(query=query))
    elif decision.action =="RAG":
        rag_chain = get_rag_chain()
        print(rag_chain.invoke({"question":query}))
    else :
        print(f"⚠️ Warning: Unknown action '{decision.action}'")
        return "I'm sorry, I wasn't sure which tool to use for that request."

def route_query(query:str):
    decision = classifier_agent.classify(query=query)
    return router_agent(query , decision)

if __name__ =="__main__":
    route_query("")