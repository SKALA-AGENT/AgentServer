# market_agent.py
import sys
# 상위 디렉토리를 Python 경로에 추가
sys.path.append(r'C:\Users\Administrator\Documents\SKALA\AgentServer')

from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from tools.web_search import web_search_tool
from tools.prompt_templates import MARKET_PROMPT, MARKET_ANALYSIS_PROMPT
from datetime import datetime
from dotenv import load_dotenv  
from util.agent_state import AgentState 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_teddynote.models import get_model_name, LLMs


load_dotenv()  #환경 변수 로드

AGENT_NAME = "시장성/경쟁력 수집"
MODEL_NAME = get_model_name(LLMs.GPT4)

#검색 에이전트 생성 함수 > 웹 겁색을 수행하고 결과를 분석하는 LangChain 체인을 생성
def create_search_agent() -> Runnable:
        """웹 검색 기반 시장 분석 에이전트 생성"""
        search = web_search_tool()          #Tavily API를 사용한 웹검색 도구 생성
        
        chain = (
            {"search_result": search.run, "question": lambda x: x}
            | MARKET_PROMPT
            | ChatOpenAI(temperature=0.1, model=MODEL_NAME)           #ChatOpenAI 모델로 분석 0.1로 일관된 응답 유도
            | StrOutputParser()                     #결과 문자열 반환
        )
        
        return chain
search_agent = create_search_agent()               #체인 저장하여 재사용
        
#데이터 수집 메인 함수  > 스타트업의 시장성과 경쟁력 정보 수집의 메인 함수    
def collect(state: AgentState = None) -> str:
        startup_name = state['company']
        """스타트업의 시장성 및 경쟁력 정보 수집
        
        Args:
            startup_name: 분석할 스타트업 기업명
            
        Returns:
            str: 시장성 및 경쟁력 분석 결과 문자열
        """
        print(f"{AGENT_NAME} 에이전트가 '{startup_name}'의 시장성/경쟁력 정보를 수집 중...")
        
        # 시장 분석 수행
        market_analysis = analyze_market(startup_name)   #market_analysis 함수를 호출하여 웹 검색 기반 시장 분석 수행
        
        # 분석 결과를 포맷팅하여 반환 (문자열 형식)
        formatted_result = format_analysis_result(startup_name, market_analysis)
        
        
        # state 업데이트 > 상태 객체(state)가 제공된 경우, 결과를 AIMessage 객체로 변환하여 상태에 저장
        if state is not None:
            result_message = AIMessage(content=formatted_result)     # AIMessage 객체로 변환
            state["market"] = list(state.get("market", [])) + [result_message]
            
        #최종적으로 포맷팅된 분석 결과 문자열을 반환
        return formatted_result 
    
#시장 분석 함수 > 웹 검색을 통해 스타트업의 시장 분석 정보를 수집
def analyze_market(startup_name: str) -> str:
        """웹 검색을 통한 시장 분석 수행
        
        Args:
            startup_name: 분석할 스타트업 기업명
            
        Returns:
            str: 시장 분석 결과 문자열
        """
        # 스타트업 정보를 바탕으로 검색 쿼리 생성
        # 일반 검색, 산업 검색, 경쟁사 검색을 균형있게 구성
        queries = [
            f"{startup_name} 기업 정보",
            f"{startup_name} 시장 규모",
            f"{startup_name} 경쟁사 분석",
            f"{startup_name} 산업 성장률",
            f"{startup_name} 시장 동향"
        ]
        
        results = []
        for query in queries:
            print(f"검색 중: '{query}'")
            try:
                search_result = search_agent.invoke(query)      #각 쿼리에 대해 search_agent를 호출하여 웹 검색 수행
                results.append(f"검색어: {query}\n결과: {search_result}")
            except Exception as e:
                print(f"검색 중 오류 발생: {e}")
                results.append(f"검색어: {query}\n결과: 검색 중 오류가 발생했습니다.")
        
        # 모든 결과를 종합 > 모든 검색 결과를 하나의 문자열로 결합
        combined_result = "\n\n".join(results)
        
        # 검색 결과가 부족하면 enhance_search_results 함수로 추가 검색 수행
        if "정보가 없습니다" in combined_result or "찾을 수 없습니다" in combined_result:
            combined_result = enhance_search_results(startup_name, combined_result)
        
        # 종합 분석 요청
        # 프롬프트 템플릿 사용
        final_analysis_prompt = MARKET_ANALYSIS_PROMPT.format(
            startup_name=startup_name,
            combined_result=combined_result
        )
        
        #최종 프롬프트를 구성하여 ChatOpenAI에 전달하고 시장 분석 요청 -> AIMessage에서 content만 추출하여 반환
        try:
            final_analysis = ChatOpenAI(temperature=0).invoke(final_analysis_prompt)   
            # AIMessage 객체 처리
            if hasattr(final_analysis, 'content'):  # AIMessage 객체인 경우
                final_analysis = final_analysis.content
            elif isinstance(final_analysis, dict) and 'content' in final_analysis:
                final_analysis = final_analysis['content']
        except Exception as e:
            print(f"분석 생성 중 오류 발생: {e}")
            final_analysis = f"분석 생성 중 오류가 발생했습니다: {str(e)}\n\n수집된 정보:\n{combined_result[:1000]}..."
        return final_analysis
    
#검색 결과 강화 함수 > 초기 결과가 충분하지 않을 때 추가 검색 수행
def enhance_search_results(startup_name: str, initial_results: str) -> str:
        """검색 결과가 불충분할 경우 추가 정보 검색
        
        Args:
            startup_name: 스타트업 기업명
            initial_results: 초기 검색 결과
            
        Returns:
            str: 강화된 검색 결과
        """
        print(f"'{startup_name}'에 대한 초기 검색 결과 불충분. 추가 검색 실행...")
        
        # 다른 키워드로 추가 검색 > 각 쿼리에 대해 검색 수행
        additional_queries = [
            f"{startup_name} 비즈니스 모델",
            f"{startup_name} 산업 보고서",
            f"{startup_name} 투자 라운드",
            f"{startup_name} 유사 기업",
            f"{startup_name} 산업 분석"
        ]
        
        additional_results = []
        for query in additional_queries:
            print(f"추가 검색 중: '{query}'")
            try:
                result = search_agent.invoke(query)
                additional_results.append(f"추가 검색: {query}\n결과: {result}")
            except Exception as e:
                print(f"추가 검색 중 오류 발생: {e}")
                additional_results.append(f"추가 검색: {query}\n결과: 검색 중 오류가 발생했습니다.")
        
        # 모든 결과 합치기 > 강화된 검색 결과 반환
        enhanced_results = initial_results + "\n\n" + "\n\n".join(additional_results)
        return enhanced_results 

#분석 결과 포맷팅 함수  
def format_analysis_result(startup_name: str, analysis: str) -> str:
        """분석 결과를 문자열 형식으로 포맷팅
        
        Args:
            startup_name: 스타트업 기업명
            analysis: 시장 분석 결과
            
        Returns:
            str: 포맷팅된 분석 보고서
        """
        # 분석 결과를 구조화된 형식으로 포맷팅
        formatted_result = f"""
        # {startup_name} 시장성 및 경쟁력 분석 보고서

        ## 분석 개요
        '{startup_name}'에 대한 시장성 및 경쟁력 분석을 수행했습니다. 아래는 주요 분석 결과입니다.

        ## 상세 분석 결과
        {analysis}

        """
        return formatted_result

   # 테스트 코드
if __name__ == "__main__":
    # 테스트 스타트업 기업명 설정
    test_startup_name = "모빌린트"  # 분석할 스타트업 기업명 입력
    
    # 기업명 입력 받기 (대화형 실행 시)
    if len(sys.argv) > 1:
        test_startup_name = sys.argv[1]
    else:
        user_input = input("분석할 스타트업 기업명을 입력하세요: ")
        if user_input.strip():
            test_startup_name = user_input.strip()
    
      # 상태 객체 생성 시도
    state = None
    try:
        state = AgentState(
            company='',
            financial=[],
            market=[],
            tech=[],
            ceo=[],
            investment=[]
        )
    except Exception as e:
        print(f"상태 객체 생성 실패: {e}")
    
    # 시장 정보 수집 실행
    market_analysis = collect(state)
    
    # 결과 출력
    print("\n===== 시장 분석 결과 =====")
    print(market_analysis)
    print("===========================")
    print(state["market"])