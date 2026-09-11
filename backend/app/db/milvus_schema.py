from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, utility

from app.db.milvus import connect

EMBEDDING_DIM = 1024

# price_hint / performance_score are "null olabilir" in the design doc, but this
# Milvus server (v2.3.5) predates nullable scalar fields (added in 2.4) — callers
# must insert a sentinel (0.0) instead of omitting the value.

_INDEX_PARAMS = {
    "index_type": "HNSW",
    "metric_type": "COSINE",
    "params": {"M": 16, "efConstruction": 200},
}


def _ensure_collection(name: str, fields: list[FieldSchema]) -> Collection:
    if utility.has_collection(name):
        return Collection(name)

    schema = CollectionSchema(fields=fields, description=name)
    collection = Collection(name=name, schema=schema)
    collection.create_index(field_name="embedding", index_params=_INDEX_PARAMS)
    return collection


def ensure_collections() -> list[str]:
    connect()
    created = []

    if not utility.has_collection("sales_conversations"):
        _ensure_collection(
            "sales_conversations",
            [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
                FieldSchema(name="product_id", dtype=DataType.VARCHAR, max_length=36),
                FieldSchema(name="channel_id", dtype=DataType.VARCHAR, max_length=36),
                FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=32),
            ],
        )
        created.append("sales_conversations")

    if not utility.has_collection("market_listings"):
        _ensure_collection(
            "market_listings",
            [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
                FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=128),
                FieldSchema(name="price_hint", dtype=DataType.FLOAT),
            ],
        )
        created.append("market_listings")

    if not utility.has_collection("own_posts"):
        _ensure_collection(
            "own_posts",
            [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
                FieldSchema(name="product_id", dtype=DataType.VARCHAR, max_length=36),
                FieldSchema(name="channel_id", dtype=DataType.VARCHAR, max_length=36),
                FieldSchema(name="performance_score", dtype=DataType.FLOAT),
            ],
        )
        created.append("own_posts")

    return created


if __name__ == "__main__":
    created = ensure_collections()
    if created:
        print("oluşturulan koleksiyonlar:", ", ".join(created))
    else:
        print("tüm koleksiyonlar zaten mevcut")
