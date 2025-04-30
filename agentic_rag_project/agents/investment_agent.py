from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI


# 투자 판단 에이전트 생성
def create_investment_agent(tools):
    return initialize_agent(tools=tools, llm=ChatOpenAI(), agent="chat-zero-shot-react-description", verbose=True) 