from langgraph.graph import StateGraph, START, END
from agents.trend_agent.state import GraphState
from agents.trend_agent.nodes import (
    extract_trends,
    scrap_contents,
    search_trends_with_naver_blog,
    filter_results,
)


def build_trend_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("search_trends_with_naver_blog", search_trends_with_naver_blog)
    graph.add_node("filter_results", filter_results)
    graph.add_node("scrap_contents", scrap_contents)
    graph.add_node("extract_trends", extract_trends)

    graph.add_edge(START, "search_trends_with_naver_blog")
    graph.add_edge("search_trends_with_naver_blog", "filter_results")
    graph.add_edge("filter_results", "scrap_contents")
    graph.add_edge("scrap_contents", "extract_trends")
    graph.add_edge("extract_trends", END)

    return graph
