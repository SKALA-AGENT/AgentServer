import os
from langchain_openai import ChatOpenAI
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools.tavily_search import TavilySearchResults
from tools.prompt_templates import CEO_AGENT_PROMPT
from tools.hybrid_retriever import load_hybrid_retriever

def extract_company_info(company_name: str, retriever) -> dict:
    """벡터 DB에서 기업 정보 조회"""
    try:
        # 기업명으로 관련 문서 검색
        docs = retriever.get_relevant_documents(company_name)
        if not docs:
            return {}
            
        # 첫 번째 문서에서 CEO 정보 추출
        metadata = docs[0].metadata
        return {
            "company_name": company_name,
            "ceo_name": metadata.get("ceo_name", "")
        }
    except Exception as e:
        print(f"기업 정보 조회 실패")
        return {}

def build_search_query(ceo_name: str, company_name: str) -> str:
    """검색 쿼리 생성"""
    base_keywords = [
        f'"{ceo_name}"',
        f'"{company_name}"',
        f'"{ceo_name} {company_name}"',
        f'"{ceo_name}" site:linkedin.com/in',
        f'"{company_name}" site:linkedin.com/company'
    ]

    semantic_keywords = [
        "CEO", "Founder", "대표", "창업자", "경력", "학력", "이력", "AI", "스타트업"
    ]

    site_filters = [
        "site:linkedin.com/in",
        "site:linkedin.com/pub",
        "site:naver.com",
        "site:wikipedia.org",
        "site:news.naver.com"
    ]

    query = " OR ".join(base_keywords) + " " + " OR ".join(semantic_keywords) + " " + " ".join(site_filters)
    return query

def run_ceo_agent(state):
    """워크플로우에서 호출되는 CEO 분석 에이전트"""
    
    # 기업 정보 추출
    
    company_name = state.get("company", "")
    if not company_name:
        return {"기업명 가져오지 못함"}
    retriever = state.get("retriever")
    if not retriever:
        return {"검색 시스템이 초기화되지 않았습니다."}
        
    company_info = extract_company_info(company_name, retriever)
    if not company_info:
        return {"벡터 DB에서 기업 정보를 찾을 수 없습니다."}
        
    ceo_name = company_info.get("ceo_name")
    if not ceo_name:
        return {"CEO 정보를 찾을 수 없습니다."}
    
    # LLM & 툴 초기화
    llm = ChatOpenAI(temperature=0.2, model="gpt-4")
    chain = CEO_AGENT_PROMPT | llm
    
    wiki = WikipediaAPIWrapper()
    tavily = TavilySearchResults(k=3)
    
    try:
        # 검색 쿼리 생성
        query = build_search_query(ceo_name, company_name)
        
        # 정보 수집
        wiki_result = wiki.run(query)
        tavily_result = tavily.run(query)
        
        # 결과 결합
        combined = f"""
Wikipedia 결과:
{wiki_result}

Tavily 결과:
{tavily_result}
"""
        
        # 프롬프트 실행 및 결과 반환
        result = chain.invoke({
            "ceo_name": ceo_name,
            "company_name": company_name,
            "search_results": combined
        })
        
        return {"ceo": result}
        
    except Exception as e:
        return {"ceo": f"CEO 정보 수집 실패"}