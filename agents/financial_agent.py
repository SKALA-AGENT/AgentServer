from langchain_core.runnables import Runnable, RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from langchain_community.chat_message_histories import ChatMessageHistory
from tools.hybrid_retriever import load_hybrid_retriever, load_dense_retriever
from typing import Dict
from tools.prompt_templates import FINANCE_PROMPT
from tools.load_docs import load_company_pdfs
from langchain_teddynote.messages import AgentStreamParser
from util.agent_state import AgentState
# 스토어 초기화
store: Dict[str, ChatMessageHistory] = {}

def create_retriever_tool(retriever, name="financial_search", description="재무 정보 검색 도구"):
    """리트리버를 도구로 변환하는 함수"""
    return Tool(
        name=name,
        func=lambda q: retriever.get_relevant_documents(q),
        description=description
    )

# def get_session_history(session_ids: str) -> ChatMessageHistory:
#     """세션 기록 관리 함수"""
#     if session_ids not in store:
#         store[session_ids] = ChatMessageHistory()
#     return store[session_ids]

def create_financial_agent(retriever) -> Runnable:
    """재무 분석 에이전트 생성"""
    # 리트리버를 도구로 변환
    retriever_tool = create_retriever_tool(
        retriever,
        name="financial_search",
        description="기업 재무 정보를 검색하는 도구입니다. 재무제표, 재무비율, 현금흐름 등의 정보를 검색할 수 있습니다."
    )
    
    # 도구 목록 정의
    tools = [retriever_tool]
    
    # LLM 정의
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    # 에이전트 생성
    agent = create_tool_calling_agent(llm, tools, FINANCE_PROMPT)
    
    # AgentExecutor 생성
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
    
    # 채팅 기록이 포함된 에이전트 생성
    # agent_with_chat_history = RunnableWithMessageHistory(
    #     agent_executor,
    #     get_session_history,
    #     input_messages_key="input",
    #     history_messages_key="chat_history"
    # )
    
    return agent_executor

def create_financial_analyse(state:AgentState):
    """재무 분석 에이전트 답변 생성"""
    # 문서 로드
    docs = load_company_pdfs(force_reload=False)
    # 리트리버 생성
    retriever = load_hybrid_retriever(
        vectordb_path="data/vectordb/financial_bge_ko",
        docs=docs
    )
    # 에이전트 생성
    agent_executor = create_financial_agent(retriever)
    # 질의 응답
    query = state["company"]
    # 스트리밍 파서 정의
    agent_stream_parser = AgentStreamParser()
    # 스트리밍 응답 처리
    response = agent_executor.stream(
        {"input": query}
    )
    # 스트림 처리
    for step in response:
        agent_stream_parser.process_agent_steps(step)
    print("-------------투자보고서-------------------")
    print(agent_stream_parser.get_response())
    print("----------------------------------------")
    res = {"financial": [agent_stream_parser.get_response()]}
    # 스트리밍 응답 반환
    return res
