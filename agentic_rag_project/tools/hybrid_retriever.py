from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from typing import List, Any


def load_hybrid_retriever(vectordb_path: str, docs: List[Any]):
    # Dense
    vectorstore = FAISS.load_local(vectordb_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    dense_retriever = vectorstore.as_retriever()

    # Sparse
    sparse_retriever = BM25Retriever.from_documents(docs)

    # Hybrid (dense + sparse)
    hybrid_retriever = EnsembleRetriever(retrievers=[dense_retriever, sparse_retriever], weights=[0.5, 0.5])
    return hybrid_retriever 