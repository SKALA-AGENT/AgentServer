from tools.hybrid_retriever import load_hybrid_retriever
from agents.financial_agent import create_financial_agent, create_financial_analyse
from util.agent_state import AgentState
from tools.load_docs import load_company_pdfs
from fastapi import FastAPI
from langchain_teddynote.messages import stream_graph, random_uuid
from langchain_core.runnables import RunnableConfig
from contextlib import asynccontextmanager
from workflows.agentic_rag_graph import create_workflow
from langchain_core.messages import HumanMessage

# 테스트 코드
if __name__ == "__main__":
    state = AgentState(
        company=HumanMessage('뤼튼테크놀로지스'),
        financial=[],
        market=[],
        tech=[],
        ceo=[],
        investment=[]
    )
    graph = create_workflow("./data/vectordb/financial_bge_ko")

    config = RunnableConfig(recursion_limit=20, configurable={"thread_id": random_uuid()})
    inputs = {
        "company": [HumanMessage(content='뤼튼테크놀로지스')]
    }
    res = graph.stream(inputs, config, stream_mode="messages")
    print(res)
