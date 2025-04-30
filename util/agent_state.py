from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    financial: Annotated[Sequence[BaseMessage], add_messages]
    market: Annotated[Sequence[BaseMessage], add_messages]
    tech: Annotated[Sequence[BaseMessage], add_messages]
    ceo: Annotated[Sequence[BaseMessage], add_messages]
    investment: Annotated[Sequence[BaseMessage], add_messages]


