from .vectorstore import connect_to_vector_store

def get_retriever():
    vs = connect_to_vector_store()
    retriever =  vs.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3
        }
    )
    return retriever