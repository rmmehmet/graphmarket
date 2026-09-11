from app.agents.providers.router import get_provider
from app.services.job_service import db_session
from app.services.settings_service import resolve_profile


def run(state: dict) -> dict:
    team_id = state["team_id"]
    extracted = state.get("extracted", {})

    with db_session() as db:
        provider_name, model_name, api_key = resolve_profile(db, team_id, "synthesis")
    provider = get_provider(provider_name, model_name, api_key)

    prompt = (
        f"'{state['category']}' kategorisi için şu çıkarım özetine dayanarak kısa "
        f"bir pazar trend raporu yaz (3-4 madde, Türkçe):\n\n{extracted.get('summary', '')}"
    )
    try:
        report_text = provider.complete(prompt)
    except Exception as exc:
        report_text = f"[sentez sağlayıcısı başarısız oldu: {exc}]\n{extracted.get('summary', '')}"

    return {
        "report": {
            "category": state["category"],
            "text": report_text,
            "sources": len(state.get("search_results", [])),
        }
    }
