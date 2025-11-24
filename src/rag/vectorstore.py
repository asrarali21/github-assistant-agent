from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from .loader import load_repo
from .embedding import get_dense_vector , get_sparse_vector
from langchain_qdrant import QdrantVectorStore


def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(docs)


def get_qdrant_client():
   return QdrantClient("localhost" , port=6333)



def create_github_vector_store(url , collection_name="github-repo-data"):
    docs = load_repo(url)
    chunk_docs=(docs)

    dense=get_dense_vector()
    sparse=get_sparse_vector()



    vector_store = QdrantVectorStore.from_documents(
        documents=chunk_docs,
        embedding=dense,
        collection_name=collection_name,
        spare_embedding=sparse
    )
    return vector_store



def get_vector_store(url:str , collection_name="github-repo-data"):
    return create_github_vector_store(url , collection_name=collection_name)
