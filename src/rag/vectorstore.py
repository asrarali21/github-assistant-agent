from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from .loader import load_repo
from .embedding import get_dense_vector , get_sparse_vector
from langchain_qdrant import QdrantVectorStore , RetrievalMode


def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(docs)


def get_qdrant_client():
   return QdrantClient("localhost" , port=6333)



def ingest_repo_to_vectorstore(url , collection_name="github-repo-data"):
    docs = load_repo(url)
    chunks = chunk_docs(docs)

    dense=get_dense_vector()
    sparse=get_sparse_vector()

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=dense,
        collection_name=collection_name,
        sparse_embedding=sparse,
        retrieval_mode = RetrievalMode.HYBRID,
        url="http://localhost:6333"
    )
    return vector_store

def connect_to_vector_store(collection_name="github-repo-data"):
    client=get_qdrant_client()
    dense=get_dense_vector()
    sparse=get_sparse_vector()

    vector_store = QdrantVectorStore(
        client=client,
        embedding=dense,
        collection_name=collection_name,
        sparse_embedding=sparse,
        retrieval_mode = RetrievalMode.HYBRID
    )
    return vector_store
