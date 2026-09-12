from app.agents.providers.claude_subscription_provider import ClaudeSubscriptionProvider


def run(state: dict) -> dict:
    """Kullanıcının Claude aboneliğinin WebSearch aracıyla gerçek arama yapar — ayrı bir
    arama API anahtarı gerekmez. Bir sorgu başarısız olursa (CLI hatası, izin sorunu vb.)
    o sorguyu atlayıp diğerlerine devam eder; hepsi başarısız olursa boş sonuç döner ve
    downstream extraction/synthesis düğümleri bunu "gerçek veri yok" olarak raporlar.
    """
    queries = state.get("queries", [])
    existing = state.get("search_results", [])
    provider = ClaudeSubscriptionProvider()

    results = []
    for q in queries:
        try:
            found = provider.search(q)
        except Exception as exc:
            results.append(
                {
                    "query": q,
                    "title": "[arama başarısız]",
                    "url": "",
                    "snippet": f"'{q}' için web araması yapılamadı: {exc}",
                }
            )
            continue

        sources = found.get("sources") or []
        results.append(
            {
                "query": q,
                "title": sources[0]["title"] if sources else q,
                "url": sources[0]["url"] if sources else "",
                "snippet": found.get("summary", ""),
                "sources": sources,
            }
        )

    return {"search_results": existing + results}
