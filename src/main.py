from fastapi import FastAPI
from src.agents.github_agent import agent
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GitHub Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    