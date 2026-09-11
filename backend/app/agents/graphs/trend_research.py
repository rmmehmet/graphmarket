from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.nodes import extraction, graph_writer, planner, search_tool, synthesis, vector_writer
from app.agents.nodes import verification as verification_node


class TrendResearchState(TypedDict, total=False):
    job_id: str
    team_id: str
    category: str
    product_id: str | None
    queries: list[str]
    search_results: list[dict]
    extracted: dict
    graph_written: bool
    vector_written: bool
    report: dict
    verified: bool
    retry_count: int
    error: str | None


def _route_after_verification(state: TrendResearchState) -> str:
    return END if state.get("verified") else "search_tool"


def build_graph():
    graph = StateGraph(TrendResearchState)

    graph.add_node("planner", planner.run)
    graph.add_node("search_tool", search_tool.run)
    graph.add_node("extraction", extraction.run)
    graph.add_node("graph_writer", graph_writer.run)
    graph.add_node("vector_writer", vector_writer.run)
    graph.add_node("synthesis", synthesis.run)
    graph.add_node("verification", verification_node.run)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "search_tool")
    graph.add_edge("search_tool", "extraction")
    graph.add_edge("extraction", "graph_writer")
    graph.add_edge("extraction", "vector_writer")
    graph.add_edge("graph_writer", "synthesis")
    graph.add_edge("vector_writer", "synthesis")
    graph.add_edge("synthesis", "verification")
    graph.add_conditional_edges(
        "verification", _route_after_verification, {"search_tool": "search_tool", END: END}
    )

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
