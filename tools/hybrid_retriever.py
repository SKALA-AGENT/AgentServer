from langchain.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.document_loaders import PyMuPDFLoader
from typing import List, Any
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
from tools.load_docs import load_company_pdfs
import os

# 파일 경로 설정
vectordb_path = "data/vectordb/financial_bge_ko"
file_path = "data/"

docs = load_company_pdfs(file_path)

# [1] 환경 변수 로드 및 설정
load_dotenv()
hf_token = os.getenv('HUGGINGFACE_TOKEN')  # .env 파일에서 HUGGINGFACE_TOKEN 불러오기

if not hf_token:
    raise ValueError("Hugging Face 토큰이 설정되지 않았습니다. .env 파일을 확인해주세요.")

# [2] 임베딩 모델 초기화
model_name = "jhgan/ko-sbert-nli"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}  # 코사인 유사도를 위한 정규화

embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

def load_dense_retriever(vectordb_path: str):
    """Dense 리트리버만 로드하는 함수"""
    try:
        # 저장된 벡터 DB 로드
        loaded_vectorstore = FAISS.load_local(
            folder_path=vectordb_path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        print("벡터 DB 로드 완료!")
        
        # Dense 리트리버 생성
        dense_retriever = loaded_vectorstore.as_retriever(
            search_type="similarity",  # similarity 검색 사용
            search_kwargs={"k": 4}     # 상위 4개 문서 반환
        )
        return dense_retriever
        
    except Exception as e:
        print(f"Dense 리트리버 로드 중 오류 발생: {e}")
        raise

def load_hybrid_retriever(vectordb_path: str, docs: List[Any]):
    # Dense
    # 저장된 벡터 DB 로드
    loaded_vectorstore = FAISS.load_local(
        folder_path=vectordb_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # 안전한 소스에서 로드할 때만 True로 설정
    )
    print("벡터 DB 로드 완료!")
    loaded_vectorstore = FAISS.load_local(vectordb_path, embeddings, allow_dangerous_deserialization=True)
    dense_retriever = loaded_vectorstore.as_retriever()

    # Sparse
    sparse_retriever = BM25Retriever.from_documents(docs)

    # Hybrid (dense + sparse)
    hybrid_retriever = EnsembleRetriever(retrievers=[dense_retriever, sparse_retriever], weights=[0.5, 0.5])
    return hybrid_retriever

# def create_retriever_tool(retriever, name="financial_search", description="재무 정보 검색 도구"):
#     """리트리버를 도구로 변환하는 함수"""
#     return Tool(
#         name=name,
#         func=lambda q: retriever.get_relevant_documents(q),
#         description=description
#     )

