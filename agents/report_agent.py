from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from tools.prompt_templates import REPORT_PROMPT


# 투자 보고서 생성 에이전트 생성
def create_report_agent():
    return LLMChain(prompt=REPORT_PROMPT, llm=ChatOpenAI()) 