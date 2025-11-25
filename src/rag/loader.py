from langchain_community.document_loaders import GitLoader


def load_repo(url : str):
    loader = GitLoader(
    clone_url=url,
    branch="main",
    repo_path="./data/repo"
)
    docs = loader.load()
    return docs






