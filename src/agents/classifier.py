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

Your job is to decide which action the system must take for the user query.

Return STRICT JSON using this schema:
{schema}

Rules:
- If the question is general GitHub knowledge → RAG
- If the question needs latest web results → SEARCH
- If the question is about a specific GitHub repo (PRs, issues, stars, commits) → GITHUB_API
"""),
            ("user", "User query: {query}")
        ]).partial(schema=parser.get_format_instructions())

    def classify(self , query) -> ClassificationResult:
        chain = self.prompt | self.llm | parser
        # the prompt expects the variable name `query` (no trailing space)
        return chain.invoke({"query": query})
    




classifier_agent = QueryClassifier()




