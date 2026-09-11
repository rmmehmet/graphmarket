def run(state: dict) -> dict:
    """Gerçek web search API henüz bağlı değil (Faz 6 kararı) — yapısal olarak doğru
    sonuç şekli döner ama içerik mock'tur. Gerçek API eklendiğinde bu dosya değişir,
    graph'ın diğer düğümleri aynı kalır.
    """
    queries = state.get("queries", [])
    existing = state.get("search_results", [])

    results = [
        {
            "query": q,
            "title": f"[mock] {q}",
            "url": "https://example.com/mock-result",
            "snippet": f"{q} için örnek pazar verisi — gerçek web search entegrasyonu henüz eklenmedi.",
        }
        for q in queries
    ]

    return {"search_results": existing + results}
