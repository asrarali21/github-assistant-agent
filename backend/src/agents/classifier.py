from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from src.config.settings import settings
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel , Field


#in the below form the llm gives the response rather than just random response 
class ClassificationResult(BaseModel):
    action:str = Field(... , description="GITHUB_PR_COUNT | GITHUB_STATS | GITHUB_CONTRIBUTORS | GITHUB_COMMITS | GITHUB_ISSUES | GITHUB_LANGUAGES | GITHUB_RELEASES | GITHUB_OVERVIEW | SEARCH | RAG")
    repo:str | None =Field(None , description="Repository full name if needed")
    reason: str = Field(... , description="Why this classification was made")




parser = PydanticOutputParser(pydantic_object=ClassificationResult)

#
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

### 1️⃣ GITHUB_PR_COUNT
Choose when user asks about:
- Pull request count or number of PRs
- Open/closed PR statistics
Examples:
- "How many open PRs are in vercel/next.js?"
- "PR count for facebook/react"

### 2️⃣ GITHUB_STATS
Choose when user asks about:
- Stars, forks, watchers count
- General repository statistics
- Repository description or info
Examples:
- "How many stars does tensorflow/tensorflow have?"
- "What are the stats for microsoft/vscode?"

### 3️⃣ GITHUB_CONTRIBUTORS
Choose when user asks about:
- Top contributors
- Who contributes to a repo
- Contribution statistics
Examples:
- "Who are the top contributors to kubernetes/kubernetes?"
- "Show contributors for nodejs/node"

### 4️⃣ GITHUB_COMMITS
Choose when user asks about:
- Recent commits
- Commit history
- Latest changes
Examples:
- "What are the recent commits in rust-lang/rust?"
- "Show me latest commits for flutter/flutter"

### 5️⃣ GITHUB_ISSUES
Choose when user asks about:
- Issue count (open/closed)
- Issue statistics
- Bug reports
Examples:
- "How many issues are open in pytorch/pytorch?"
- "Issue stats for angular/angular"

### 6️⃣ GITHUB_LANGUAGES
Choose when user asks about:
- Programming languages used
- Language breakdown/distribution
- Tech stack
Examples:
- "What languages are used in docker/docker?"
- "Language breakdown for django/django"

### 7️⃣ GITHUB_RELEASES
Choose when user asks about:
- Latest release
- Release versions
- Download counts
Examples:
- "What is the latest release of electron/electron?"
- "Show releases for vuejs/vue"

### 8️⃣ GITHUB_OVERVIEW
Choose when user asks for:
- General overview of a repository
- Summary of a project
- Multiple metrics at once
Examples:
- "Tell me about vercel/next.js"
- "Give me an overview of facebook/react"
- "What is the golang/go repository?"

### 9️⃣ SEARCH
Choose **SEARCH** only when:
- The query is a general internet question (not repo-specific)
- The user wants something outside GitHub
Examples:
- "Latest news about GitHub Actions"
- "Search tutorials on GitHub PR workflow"

### 🔟 RAG
Choose **RAG** when:
- User asks about code content, file structure
- Wants to understand how something works in the repo
- Question and answer about repository internals
Examples:
- "How does authentication work in this repo?"
- "Explain the folder structure of vercel/next.js"

## Output fields:
- action = GITHUB_PR_COUNT | GITHUB_STATS | GITHUB_CONTRIBUTORS | GITHUB_COMMITS | GITHUB_ISSUES | GITHUB_LANGUAGES | GITHUB_RELEASES | GITHUB_OVERVIEW | SEARCH | RAG
- repo = repository name in 'owner/repo' format OR null
- reason = clear explanation of classification
"""),
    ("user", "User query: {query}")
        ]).partial(schema=parser.get_format_instructions())

    def classify(self , query) -> ClassificationResult:
        chain = self.prompt | self.llm | parser
        return chain.invoke({"query": query})
    




classifier_agent = QueryClassifier()




