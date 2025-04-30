from langchain.tools.tavily_search import TavilySearchResults


def web_search_tool():
    return TavilySearchResults(k=3) 