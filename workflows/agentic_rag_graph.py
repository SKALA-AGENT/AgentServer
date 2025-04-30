from langgraph.graph import StateGraph, END
from agents.financial_agent import create_financial_agent
from agents.tech_agent import create_search_agent
from agents.market_agent import create_search_agent as create_market_agent
from agents.investment_agent import create_investment_agent
from agents.report_agent import create_report_agent
from tools.hybrid_retriever import load_hybrid_retriever
from agents.ceo_agent import run_ceo_agent
from typing import Dict, Any


# 각 에이전트의 결과를 수집하여 supervisor에게 전달
def process_agent_results(state: Dict[str, Any]):
    return {
        "financial_result": state.get("financial", ""),
        "tech_result": state.get("tech", ""),
        "market_result": state.get("market", ""),
        "ceo_result": state.get("ceo", {}).get("ceo", "정보 없음")
    }

# 투자 보고서 생성 워크플로우
def create_workflow(vectordb_path: str, docs):
    # Initialize retrievers and agents
    hybrid_retriever = load_hybrid_retriever(vectordb_path, docs)
    
    financial_agent = create_financial_agent(hybrid_retriever)
    tech_agent = create_search_agent("Tech Info")
    market_agent = create_market_agent("Market Info")
    investment_agent = create_investment_agent([])  # Add tools as needed
    report_agent = create_report_agent()

    # Define workflow
    workflow = StateGraph()
    
    # Add nodes for parallel execution
    workflow.add_node("financial", financial_agent)
    workflow.add_node("tech", tech_agent)
    workflow.add_node("market", market_agent)
    workflow.add_node("collect_results", process_agent_results)
    workflow.add_node("invest", investment_agent)
    workflow.add_node("report", report_agent)
    workflow.add_node("ceo", run_ceo_agent)
    workflow.add_node("collect_results", process_agent_results)

    # Define parallel execution flow
    workflow.set_entry_point("financial")
    workflow.set_entry_point("ceo")

    # Parallel agent execution
    workflow.add_edge("financial", "collect_results")
    workflow.add_edge("tech", "collect_results")
    workflow.add_edge("market", "collect_results")
    workflow.add_edge("ceo", "collect_results")
    
    # Results to supervisor
    workflow.add_edge("collect_results", "invest")
    workflow.add_edge("invest", "report")
    workflow.add_edge("report", END)
    workflow.add_edge("collect_results", END)
    # Enable parallel execution
    workflow.set_parallel_execution(["financial", "tech", "market"])

    return workflow.compile() 