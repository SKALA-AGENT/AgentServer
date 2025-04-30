from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from tools.web_search import web_search_tool
from tools.prompt_templates import MARKET_PROMPT


# 시장 분석 에이전트 생성
def create_search_agent(name: str) -> Runnable:
    search = web_search_tool()
    
    chain = (
        {"search_result": search.run, "question": lambda x: x}
        | MARKET_PROMPT
        | ChatOpenAI()
        | StrOutputParser()
    )
    
    return chain 