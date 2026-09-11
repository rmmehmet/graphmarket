from pymilvus import Collection

from app.agents.embeddings import placeholder_embedding
from app.db.milvus import connect


def run(state: dict) -> dict:
    connect()
    extracted = state.get("extracted", {})
    text = (extracted.get("summary") or state["category"])[:2000]
    embedding = placeholder_embedding(text)

    collection = Collection("market_listings")
    collection.insert([[embedding], [text], [state["category"]], [0.0]])
    collection.flush()

    return {"vector_written": True}
