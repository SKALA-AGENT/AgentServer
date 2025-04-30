from agents.financial_agent import create_financial_agent
from tools.load_docs import load_company_pdfs
from tools.hybrid_retriever import load_hybrid_retriever, load_dense_retriever
from langchain_teddynote.messages import AgentStreamParser

# 테스트 코드
if __name__ == "__main__":
    # Agent 파서 정의
    agent_stream_parser = AgentStreamParser()

    # 문서 로드 (캐시된 파일 사용)
    docs = load_company_pdfs(force_reload=False)  # 첫 실행시에만 True로 설정
    
    # 하이브리드 리트리버 생성
    hybrid_retriever = load_hybrid_retriever(
        vectordb_path="data/vectordb/financial_bge_ko",
        docs=docs
    )
    
    # 에이전트 생성
    financial_agent = create_financial_agent(hybrid_retriever)
    
    # 테스트 쿼리 목록
    test_queries = [
        "뤼튼테크놀로지스의 CEO는 누구야?",
        "네오사피엔스의 영업이익률은 어떤가요?",
        "모두싸인의 부채비율과 유동비율을 분석해주세요."
    ]
    
    # 스트리밍 테스트 실행
    print("=== 재무 분석 에이전트 스트리밍 테스트 ===\n")
    
    for query in test_queries:
        print(f"질문: {query}")
        try:
            # 스트리밍 응답 처리
            response = financial_agent.stream(
                {"input": query},
                config={"configurable": {"session_id": "SKALA-002"}}
            )
            
            # 스트림 처리
            for step in response:
                agent_stream_parser.process_agent_steps(step)
                
            print("-" * 80 + "\n")
            
        except Exception as e:
            print(f"에러 발생: {str(e)}\n")

    # 일반 테스트 실행
    print("=== 재무 분석 에이전트 일반 테스트 ===\n")
    
    for query in test_queries:
        print(f"질문: {query}")
        try:
            response = financial_agent.invoke({
                "input": query,
                "session_id": "test_session"
            })
            print(f"응답: {response}\n")
            print("-" * 80 + "\n")
        except Exception as e:
            print(f"에러 발생: {str(e)}\n")