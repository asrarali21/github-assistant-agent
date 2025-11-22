import os
from langchain_community.document_loaders import GitLoader
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Ensure you have your API key set
# os.environ["OPENAI_API_KEY"] = "sk-..."

def ingest_repository(repo_url: str, local_path: str = "./temp_repo"):
    """
    Clones a repo, splits the code, and creates a vector store.
    """
    print(f"--- Cloning {repo_url} ---")
    
    # 1. Load the Repository
    # We filter for code files only (py, js, ts, etc.) to avoid junk
    loader = GitLoader(
        clone_url=repo_url,
        repo_path=local_path,
        branch="main",
        file_filter=lambda file_path: file_path.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".md"))
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} files.")

    # 2. Split the Code (Context Aware)
    # We use a splitter that understands code structure (classes, functions)
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, # You can make this dynamic based on repo type
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")

    # 3. Create Vector Store (ChromaDB)
    # This creates a local database in the 'db_storage' folder
    vector_db = Chroma.from_documents(
        documents=texts, 
        embedding=OpenAIEmbeddings(),
        persist_directory="./db_storage" 
    )
    print("--- Ingestion Complete ---")
    return vector_db