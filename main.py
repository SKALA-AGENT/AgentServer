from fastapi import FastAPI
from langchain_teddynote.messages import stream_graph, random_uuid
from langchain_core.runnables import RunnableConfig
from contextlib import asynccontextmanager
from workflows.agentic_rag_graph import create_workflow

graph = create_workflow("./data/vectordb/financial_bge_ko")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    graph = create_workflow("./data/vectordb/financial_bge_ko")
    yield
    # Clean up the ML models and release the resources
    



app = FastAPI(lifespan=lifespan)




@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/agent")
async def post_agent(agent: str):
    config = RunnableConfig(recursion_limit=20, configurable={"thread_id": random_uuid()})
    inputs = {
        "company": [
        ("user", agent),
        ]
    }
    res = graph.stream(inputs, config, stream_mode="messages")
    # stream_graph(graph, inputs, config, ['financial', 'tech', 'market', 'ceo', 'investment','report'])
    return {"received_agent": res} 