from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from src.config.settings import settings
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel , Field



class ClassificationResult(BaseModel):
    action:str = Field(... , description="RAG | SEARCH | GITHUB_API")
    repo:str | None =Field(None , description="Repository full name if needed")
    reason: str = Field(... , description="Why this classification was made")




parser = PydanticOutputParser(pydantic_object=ClassificationResult)


class QueryClassifier:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            temperature=0,
            google_api_key=settings.GEMINI_API_KEY
        )
        self.prompt=ChatPromptTemplate.from_messages([
            ("system", """
You are a routing classifier for a GitHub Assistant.

Your output determines which internal tool should be called.

Return STRICT JSON in this schema:
{schema}

## CLASSIFICATION RULES

### 1️⃣ GITHUB_API
Choose **GITHUB_API** when:
- The question is about a specific GitHub repository.
- Mentions patterns like: `owner/repo`
- Involves:
  - open PR count
  - issues count
  - stars
  - forks
  - contributors
  - commits
  - branches
  - release tags
  - workflows
  - CI/CD status
Examples:
- "How many open PRs are in vercel/next.js?"
- "List issues in microsoft/vscode"
- "How many stars does vercel/next.js have?"

### 2️⃣ SEARCH
Choose **SEARCH** only when:
- The query is a general internet question (not repo-specific).
- The user wants something outside GitHub.
Examples:
- "Latest news about GitHub Actions"
- "Search tutorials on GitHub PR workflow"
- "Find top GitHub repos about machine learning"

### 3️⃣ RAG
Choose **RAG** when:
- The query is about **GitHub concepts / knowledge**, NOT repo-specific.
Examples:
- "How to raise a PR?"
- "What is a pull request?"
- "What is GitHub Actions?"
- "Explain merge conflicts."

## Output fields:
- action = RAG | SEARCH | GITHUB_API
- repo = repository name in 'owner/repo' format OR null
- reason = clear explanation of classification
"""),
    ("user", "User query: {query}")
        ]).partial(schema=parser.get_format_instructions())

    def classify(self , query) -> ClassificationResult:
        chain = self.prompt | self.llm | parser
        return chain.invoke({"query": query})
    




classifier_agent = QueryClassifier()




