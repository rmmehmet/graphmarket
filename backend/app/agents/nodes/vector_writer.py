import hashlib

from pymilvus import Collection

from app.db.milvus import connect
from app.db.milvus_schema import EMBEDDING_DIM


def _placeholder_embedding(text: str) -> list[float]:
    """Gerçek embedding modeli (bge-m3) henüz bağlanmadı — bu deterministik sözde-vektör
    Milvus yazma/okuma yolunu doğrular. Gerçek model eklendiğinde bu fonksiyon değişir.
    """
    seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)
    return [((seed >> (i % 64)) % 1000) / 1000.0 for i in range(EMBEDDING_DIM)]


def run(state: dict) -> dict:
    connect()
    extracted = state.get("extracted", {})
    text = (extracted.get("summary") or state["category"])[:2000]
    embedding = _placeholder_embedding(text)

    collection = Collection("market_listings")
    collection.insert([[embedding], [text], [state["category"]], [0.0]])
    collection.flush()

    return {"vector_written": True}
