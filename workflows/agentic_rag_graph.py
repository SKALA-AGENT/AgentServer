from langgraph.graph import StateGraph, END, START
from agents.financial_agent import create_financial_agent
from agents.tech_agent import create_tech_analysis_agent
from agents.market_agent import collect
from agents.investment_agent import create_investment_agent
from agents.report_agent import generate_report_from_state
from tools.hybrid_retriever import load_hybrid_retriever
from agents.ceo_agent import run_ceo_agent
from typing import Dict, Any
from util.agent_state import AgentState


# # 각 에이전트의 결과를 수집하여 supervisor에게 전달
# def process_agent_results(state: Dict[str, Any]):
#     return {
#         "financial_result": state.get("financial", ""),
#         "tech_result": state.get("tech", ""),
#         "market_result": state.get("market", ""),
#         "ceo_result": state.get("ceo", {}).get("ceo", "정보 없음")
#     }

# 투자 보고서 생성 워크플로우
def create_workflow(vectordb_path: str):
    # # Initialize retrievers and agents
    # hybrid_retriever = load_hybrid_retriever(vectordb_path, docs)
    
    # financial_agent = create_financial_agent(hybrid_retriever)
    # tech_agent = create_search_agent("Tech Info")
    # market_agent = create_market_agent("Market Info")
    # investment_agent = create_investment_agent([])  # Add tools as needed
    # report_agent = create_report_agent()

    # Define workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes for parallel execution
    workflow.add_node("financial_", create_financial_agent)
    workflow.add_node("tech_", create_tech_analysis_agent)
    workflow.add_node("market_", collect)
    # workflow.add_node("collect_results", process_agent_results)
    workflow.add_node("ceo_", run_ceo_agent)
    workflow.add_node("investment_", create_investment_agent)
    workflow.add_node("report_", generate_report_from_state)
    # workflow.add_node("collect_results", process_agent_results)

    # # Define parallel execution flow
    # workflow.set_entry_point("financial")
    # workflow.set_entry_point("ceo")

    # Parallel agent execution
    workflow.add_edge(START, "financial_")
    workflow.add_edge("financial_", "tech_")
    workflow.add_edge("tech_", "market_")
    workflow.add_edge("market_", "ceo_")
    workflow.add_edge("ceo_", "investment_")
    workflow.add_edge("investment_", "report_")
    workflow.add_edge("report_", END)

    return workflow.compile() 