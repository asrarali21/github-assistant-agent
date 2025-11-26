from fastapi import FastAPI
from src.agents.github_agent import agent
from pydantic import BaseModel


app = FastAPI(title="GitHub Assistant API")




class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    user_query = request.query

    response = agent.run(user_query)
    return {"response": response}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

    