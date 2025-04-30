from tools.hybrid_retriever import load_hybrid_retriever
from agents.financial_agent import create_financial_agent, create_financial_analyse
from langchain.schema import AgentState
from tools.load_docs import load_company_pdfs

# 테스트 코드
if __name__ == "__main__":
    print("=== 재무 분석 에이전트 테스트 ===\n")

    # 1. 문서 로드 (캐시된 파일 사용)
    docs = load_company_pdfs(force_reload=False)  # 첫 실행시에만 True로 설정
    
    # 2. 하이브리드 리트리버 생성
    hybrid_retriever = load_hybrid_retriever(
        vectordb_path="data/vectordb/financial_bge_ko",
        docs=docs
    )
    
    # 3. 에이전트 생성
    agent_executor = create_financial_agent(hybrid_retriever)
    
    # 4. 테스트할 기업 목록
    test_companies = [
        "뤼튼테크놀로지스",
        "네오사피엔스",
        "모두싸인"
    ]
    
    # 5. 각 기업별 테스트 실행
    for company in test_companies:
        print(f"\n[{company} 분석 시작]")
        try:
            # 상태 생성
            test_state = AgentState({"company": f"{company}의 재무상태를 분석해주세요."})
            
            # 분석 실행
            response = create_financial_analyse(agent_executor, test_state)
            
            # 결과 출력
            print(f"\n[{company} 분석 결과]")
            print(response)
            print("-" * 80)
            
        except Exception as e:
            print(f"에러 발생 ({company}): {str(e)}")
            print("-" * 80)