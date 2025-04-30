#web_search.py
from langchain_community.tools.tavily_search import TavilySearchResults 
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def web_search_tool():
    """웹 검색 도구 생성
    
    Returns:
        웹 검색 도구 인스턴스
    """
    # Tavily API 키가 환경 변수에 설정되어 있어야 함
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    # 검색 도구 생성
    search = TavilySearchResults(
        max_results=5,  # 검색 결과 수
        api_key=api_key
    )
    
    return search

# 대체 검색 도구 예시 (Tavily API를 사용할 수 없는 경우)
def alternative_search_tool():
    """대체 웹 검색 도구 생성"""
    from langchain.tools import Tool
    from langchain.utilities import GoogleSearchAPIWrapper
    
    # Google 검색 API 사용 예시
    search = GoogleSearchAPIWrapper()
    
    tool = Tool(
        name="Google Search",
        description="Search Google for recent results.",
        func=search.run
    )
    
    return tool

# 대체 검색 함수 (API 없이 직접 구현)
def simple_web_search(query: str) -> str:
    """간단한 웹 검색 함수 (API 없이 직접 구현)
    
    Args:
        query: 검색 쿼리
        
    Returns:
        str: 검색 결과
    """
    import requests
    from bs4 import BeautifulSoup
    
    # 네이버 검색 예시
    url = f"https://search.naver.com/search.naver?query={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 검색 결과 추출 (네이버 검색 결과 구조에 맞게 조정 필요)
        results = []
        for item in soup.select(".total_wrap .total_tit")[:5]:  # 상위 5개 결과만
            results.append(item.text.strip())
        
        # 결과 문자열 생성
        return "\n".join(results) if results else "검색 결과가 없습니다."
    
    except Exception as e:
        return f"검색 중 오류 발생: {str(e)}"