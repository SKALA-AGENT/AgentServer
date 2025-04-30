from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from tools.prompt_templates import FINANCE_PROMPT


# 재무 분석 에이전트 생성
def create_financial_agent(retriever) -> Runnable:
    return FINANCE_PROMPT | retriever | ChatOpenAI() | StrOutputParser() 