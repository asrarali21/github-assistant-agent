from src.agents.router import route_query
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

class GitHubAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        self.synthesizer_prompt = ChatPromptTemplate.from_template("""
        You are a helpful GitHub Assistant.
        
        The user asked: "{query}"
        
        I have gathered the following information from my tools:
        "{tool_output}"
        
        Please synthesize this information into a friendly, clear, and concise answer for the user.
        If the tool output indicates an error or lack of information, apologize and explain.
        """)
        
        self.synthesizer_chain = self.synthesizer_prompt | self.llm | StrOutputParser()

    def run(self, query: str):
        print(f"🤖 Processing: {query}")
        
        # 1. Route the query and get raw data
        raw_result = route_query(query)
        
        # 2. Synthesize the final answer
        final_answer = self.synthesizer_chain.invoke({
            "query": query,
            "tool_output": raw_result
        })
        
        return final_answer

# Singleton instance
agent = GitHubAgent()

if __name__ == "__main__":
    # Test run
    response = agent.run("what is the latest update in the github?")
    print("\nFinal Answer:\n", response)
