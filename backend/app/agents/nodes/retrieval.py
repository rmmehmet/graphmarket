from pymilvus import Collection

from app.agents.embeddings import placeholder_embedding
from app.db.milvus import connect
from app.db.neo4j import get_session


def run(state: dict) -> dict:
    team_id = state["team_id"]
    question = state["question"]
    context_product_id = state.get("context_product_id")

    with get_session() as session:
        result = session.run(
            "MATCH (p:Product {team_id: $team_id}) "
            "WHERE $product_id IS NULL OR p.id = $product_id "
            "RETURN p.id AS id, p.name AS name, p.category AS category LIMIT 5",
            team_id=team_id,
            product_id=context_product_id,
        )
        products = [dict(r) for r in result]

    connect()
    embedding = placeholder_embedding(question)
    market_hits: list[dict] = []
    try:
        collection = Collection("market_listings")
        collection.load()
        search_result = collection.search(
            data=[embedding],
            anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"ef": 64}},
            limit=3,
            output_fields=["text", "category"],
        )
        market_hits = [
            {"text": hit.entity.get("text"), "category": hit.entity.get("category")}
            for hit in search_result[0]
        ]
    except Exception:
        market_hits = []

    citations = [{"type": "product", "id": p["id"], "label": p["name"]} for p in products]
    citations += [{"type": "market_listing", "id": None, "label": (h["text"] or "")[:80]} for h in market_hits]

    context_lines = [f"Ürün: {p['name']} (kategori: {p['category']})" for p in products]
    context_lines += [f"Pazar notu: {h['text']}" for h in market_hits]
    context_text = "\n".join(context_lines) or "İlgili kayıt bulunamadı."

    synthesis_prompt = (
        f"Kullanıcının sorusu: {question}\n\n"
        f"Elindeki veri:\n{context_text}\n\n"
        "Bu veriye dayanarak soruyu kısa ve net şekilde Türkçe cevapla. "
        "Veri yetersizse bunu açıkça belirt."
    )

    return {
        "citations": citations,
        "evidence_count": len(citations),
        "synthesis_prompt": synthesis_prompt,
    }
