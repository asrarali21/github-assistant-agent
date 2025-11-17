from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from src.config.settings import settings


# Step 1: Define expected output JSON schema using Pydantic
class ClassificationResult(BaseModel):
    action: str           # RAG | SEARCH | GITHUB_API
    repo: str | None = None
    reason: str


# Step 2: Build Classifier Agent
class QueryClassifier:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )

    def classify(self, query: str) -> ClassificationResult:
        system_prompt = """
You are a routing classifier for a GitHub Assistant.

Decide which action the system must take for the user query.
Return JSON only, with keys: action, repo, reason.

Rules:
- If question is general GitHub knowledge → action = "RAG"
- If question needs latest data → action = "SEARCH"
- If question is about a specific repo (PRs, commits, stars) → action = "GITHUB_API"
"""

        user_prompt = f"User query: {query}\nReturn JSON only."

        response = self.llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        # Parse into Pydantic model
        return ClassificationResult.model_validate_json(response.content)


# Utility function for outside use
classifier = QueryClassifier()