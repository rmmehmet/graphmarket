from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.nodes import extraction, graph_writer, vector_writer


class MessengerExtractionState(TypedDict, total=False):
    job_id: str
    team_id: str
    message_text: str
    customer_ref: str
    channel_id: str | None
    source: str
    extracted: dict
    matched_product_id: str | None
    graph_written: bool
    vector_written: bool


def build_graph():
    """Planlayıcı/Doğrulama yok — akış sabit ve tek yönlü, girdi tek mesaj metni."""
    graph = StateGraph(MessengerExtractionState)

    graph.add_node("extraction", extraction.run)
    graph.add_node("graph_writer", graph_writer.run)
    graph.add_node("vector_writer", vector_writer.run)

    graph.set_entry_point("extraction")
    graph.add_edge("extraction", "graph_writer")
    graph.add_edge("graph_writer", "vector_writer")
    graph.add_edge("vector_writer", END)

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
