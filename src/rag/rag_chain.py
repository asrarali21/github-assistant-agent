from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(retriever):
     llm = ChatGoogleGenerativeAI(
        model_name="gemini-2.0-flash",
        temperature=0.7,
      google_api_key=os.getenv("GEMINI_API_KEY"
      ))

   template = """You are a technical assistant for GitHub repositories.
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:"""


    prompt = ChatPromptTemplate.from_template(template)


    rag_chain = (
        {"context":retriever | format_docs , "question":}

        |prompt
        |llm
        |StrOutputParser()
    )

    return rag_chain


    

