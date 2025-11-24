from langchain_community.document_loaders import GitLoader



loader = GitLoader(
    clone_url="https://github.com/asrarali21/Quick-Diagnostics",
    branch="main",
    repo_path="./data/repo"
)

docs = loader.load()

print(docs)





