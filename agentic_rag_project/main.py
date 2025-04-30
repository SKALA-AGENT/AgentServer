import os
from dotenv import load_dotenv
from workflows.agentic_rag_graph import create_workflow


def run_agentic_rag(input_query: str, vectordb_path: str, docs):
    # Load environment variables
    load_dotenv()
    
    # Create and run workflow
    graph = create_workflow(vectordb_path, docs)
    result = graph.invoke({"question": input_query})
    return result


if __name__ == "__main__":
    # Example usage
    query = "이 기업에 투자할 가치가 있을까?"
    vectordb_path = "data/vectordb"
    docs = []  # Add your documents here
    
    result = run_agentic_rag(query, vectordb_path, docs)
    print(result) 