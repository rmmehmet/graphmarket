from app.agents.providers.router import get_provider
from app.services.job_service import db_session
from app.services.settings_service import resolve_profile


def run(state: dict) -> dict:
    team_id = state["team_id"]
    search_results = state.get("search_results", [])
    combined_text = "\n".join(r["snippet"] for r in search_results)

    with db_session() as db:
        provider_name, model_name, api_key = resolve_profile(db, team_id, "extraction")
    provider = get_provider(provider_name, model_name, api_key)

    prompt = (
        "Aşağıdaki pazar araştırma metinlerinden kategori, fiyat aralığı ve trend yönü "
        f"(yükseliş/düşüş/durağan) çıkar, kısa madde listesi olarak yaz:\n\n{combined_text}"
    )
    try:
        summary = provider.complete(prompt)
    except Exception as exc:
        summary = f"[çıkarım sağlayıcısı başarısız oldu, ham veri kullanıldı: {exc}]\n{combined_text}"

    return {
        "extracted": {
            "summary": summary,
            "source_count": len(search_results),
            "direction": "durağan",
            "strength": 0.5,
        }
    }
