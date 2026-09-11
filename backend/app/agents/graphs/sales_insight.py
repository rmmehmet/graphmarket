from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.nodes import planner, retrieval, synthesis
from app.agents.nodes import verification as verification_node


class SalesInsightState(TypedDict, total=False):
    job_id: str | None
    team_id: str
    question: str
    context_product_id: str | None
    citations: list[dict]
    evidence_count: int
    synthesis_prompt: str
    synthesis_output: str
    verified: bool
    retry_count: int
    error: str | None


def _route_after_verification(state: SalesInsightState) -> str:
    return END if state.get("verified") else "retrieval"


def build_graph():
    graph = StateGraph(SalesInsightState)

    graph.add_node("planner", planner.run)
    graph.add_node("retrieval", retrieval.run)
    graph.add_node("synthesis", synthesis.run)
    graph.add_node("verification", verification_node.run)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "retrieval")
    graph.add_edge("retrieval", "synthesis")
    graph.add_edge("synthesis", "verification")
    graph.add_conditional_edges(
        "verification", _route_after_verification, {"retrieval": "retrieval", END: END}
    )

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
