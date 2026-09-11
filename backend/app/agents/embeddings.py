import hashlib

EMBEDDING_DIM = 1024


def placeholder_embedding(text: str) -> list[float]:
    """Gerçek embedding modeli (bge-m3) henüz bağlanmadı — bu deterministik sözde-vektör
    Milvus yazma/okuma yolunu doğrular. Gerçek model eklendiğinde bu fonksiyon değişir,
    onu çağıran düğümler (vector_writer, retrieval) aynı kalır.
    """
    seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)
    return [((seed >> (i % 64)) % 1000) / 1000.0 for i in range(EMBEDDING_DIM)]
