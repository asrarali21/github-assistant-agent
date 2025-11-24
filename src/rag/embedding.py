
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_qdrant import FastEmbedSparse
google_apikey=os.getenv("GEMINI_API_KEY")

def get_dense_vector():

    dense_vector= GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=google_apikey
    )
    return dense_vector



def get_sparse_vector():
    sparse_vector=FastEmbedSparse(model_name="Qdrant/bm25")
    return sparse_vector