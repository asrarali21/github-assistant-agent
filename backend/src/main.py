from fastapi import FastAPI ,HTTPException
from src.agents.github_agent import agent
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os
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
  
  try:
        user_query = request.query
        response = agent.run(user_query)
        return {"response": response}
  except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

    