from langchain_community.document_loaders import PDFPlumberLoader
from typing import List, Dict
import os
import pickle

file_path = "data/"

def save_docs_to_pickle(docs, pickle_path="data/processed/docs.pkl"):
    """문서를 pickle 파일로 저장"""
    # 디렉토리가 없으면 생성
    os.makedirs(os.path.dirname(pickle_path), exist_ok=True)
    
    with open(pickle_path, 'wb') as f:
        pickle.dump(docs, f)
    print(f"문서가 {pickle_path}에 저장되었습니다.")

def load_docs_from_pickle(pickle_path="data/processed/docs.pkl"):
    """pickle 파일에서 문서 로드"""
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as f:
            docs = pickle.load(f)
        print(f"문서를 {pickle_path}에서 로드했습니다.")
        return docs
    return None

# [1] 기업 PDF 문서 로드
def load_company_pdfs(pdf_directory: str = "data", force_reload: bool = False) -> List[Dict]:
    pickle_path = "data/processed/docs.pkl"
    
    # force_reload가 False이고 pickle 파일이 있으면 pickle에서 로드
    if not force_reload:
        docs = load_docs_from_pickle(pickle_path)
        if docs is not None:
            return docs
    
    # pickle 파일이 없거나 force_reload가 True면 PDF에서 로드
    print("=== PDF 문서 로드 시작 ===")
    company_docs = []
    total_companies = 0

    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            # 파일명에서 기업 정보 추출
            # 예: 기업분석_보고서_국문_뤼튼테크놀로지스_202504300900.pdf
            company_info = filename.split('_')
            company_name = company_info[3]  # 기업명 추출
            report_date = company_info[4].replace('.pdf', '')  # 날짜 추출
            
            file_path = os.path.join(pdf_directory, filename)
            
            try:
                print(f"\n로딩 중: {company_name}")
                loader = PDFPlumberLoader(file_path)
                docs = loader.load()
                
                # 각 페이지에 기업 정보 메타데이터 추가
                for doc in docs:
                    doc.metadata.update({
                        'company_name': company_name,
                        'report_date': report_date,
                        'source_file': filename
                    })
                
                company_docs.extend(docs)
                total_companies += 1
                print(f"완료: {company_name} ({len(docs)} 페이지)")
                
            except Exception as e:
                print(f"에러 발생 ({filename}): {str(e)}")
    
    print(f"\n=== 로드 완료 ===")
    print(f"총 처리된 기업 수: {total_companies}")
    print(f"총 페이지 수: {len(company_docs)}")
    
    # 로드된 문서를 pickle로 저장
    save_docs_to_pickle(company_docs, pickle_path)
    
    return company_docs


# [3] 실행
# pdf_directory = file_path
# docs = load_company_pdfs(pdf_directory)

# # [4] 로드된 문서 확인
# def check_loaded_docs(docs):
#     print("\n=== 로드된 문서 확인 ===")
    
#     # 기업별 페이지 수 집계
#     company_pages = {}
#     for doc in docs:
#         company_name = doc.metadata['company_name']
#         company_pages[company_name] = company_pages.get(company_name, 0) + 1
    
#     print("\n기업별 페이지 수:")
#     for company, pages in company_pages.items():
#         print(f"{company}: {pages}페이지")
    
#     # 샘플 메타데이터 확인
#     print("\n첫 번째 문서의 메타데이터:")
#     print(docs[0].metadata)

# 로드된 문서 확인 실행
# check_loaded_docs(docs)