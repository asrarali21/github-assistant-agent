from langchain_community.document_loaders import GitLoader


import shutil
import os

def load_repo(url : str):
    repo_path = "./data/repo"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        
    loader = GitLoader(
        clone_url=url,
        branch="main",
        repo_path=repo_path,
        file_filter=lambda file_path: file_path.endswith((".py", ".md", ".txt", ".json", ".toml" , ".js" , ".ts" , ".html" , ".css" , "java"))
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {url}")
    for doc in docs:
        print(f"   - {doc.metadata.get('source', 'Unknown')}")
    return docs










