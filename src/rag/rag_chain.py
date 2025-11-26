import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def format_docs(docs):
    print("\n--- 🔍 RAG CHEF FOUND THESE INGREDIENTS ---")
    for i, doc in enumerate(docs):
        # Print the filename (source) and a snippet of content
        source = doc.metadata.get('source', 'Unknown Source')
        print(f"📄 Ingredient {i+1}: {source}")
        print(f"   Content Snippet: {doc.page_content[:100]}...\n")
    print("-------------------------------------------\n")

    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(retriever):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

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
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
