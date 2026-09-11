from pymilvus import Collection

from app.agents.embeddings import placeholder_embedding
from app.db.milvus import connect


def run(state: dict) -> dict:
    connect()
    if "message_text" in state:
        return _run_messenger(state)
    return _run_trend(state)


def _run_trend(state: dict) -> dict:
    extracted = state.get("extracted", {})
    text = (extracted.get("summary") or state["category"])[:2000]
    embedding = placeholder_embedding(text)

    collection = Collection("market_listings")
    collection.insert([[embedding], [text], [state["category"]], [0.0]])
    collection.flush()

    return {"vector_written": True}


def _run_messenger(state: dict) -> dict:
    text = state["message_text"][:2000]
    embedding = placeholder_embedding(text)

    collection = Collection("sales_conversations")
    collection.insert(
        [
            [embedding],
            [text],
            [state.get("matched_product_id") or ""],
            [state.get("channel_id") or ""],
            [state.get("source", "messenger_export")],
        ]
    )
    collection.flush()

    return {"vector_written": True}
