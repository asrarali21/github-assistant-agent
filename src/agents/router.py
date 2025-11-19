from src.agents.classifier import classifier_agent , ClassificationResult

def router_agent(decision : ClassificationResult):
    print(f"Routing to {decision.action} | Context {decision.repo}")

    if decision.action == "GITHUB_API":
         print("running github api")
    elif decision.action == "SEARCH":
        print("running search")
    elif decision.action =="RAG":
         print("running RAG")
    else :
        print(f"⚠️ Warning: Unknown action '{decision.action}'")
        return "I'm sorry, I wasn't sure which tool to use for that request."

def route_query(query:str):
    decision = classifier_agent.classify(query=query)
    return router_agent(decision)

if __name__ =="__main__":
    route_query("How many open PRs in vercel/next.js?")