from app.agents.providers.router import get_provider
from app.services.job_service import db_session
from app.services.settings_service import resolve_profile


def run(state: dict) -> dict:
    """Trend Research ve Sales Insight aynı Sentez düğümünü paylaşır — önceki düğüm
    (extraction / retrieval) `synthesis_prompt` alanını hazırlar, bu düğüm sadece
    'synthesis' node profiline göre modeli çağırır.
    """
    team_id = state["team_id"]
    prompt = state.get("synthesis_prompt", "")

    with db_session() as db:
        provider_name, model_name, api_key = resolve_profile(db, team_id, "synthesis")
    provider = get_provider(provider_name, model_name, api_key)

    try:
        output = provider.complete(prompt)
    except Exception as exc:
        output = f"[sentez sağlayıcısı başarısız oldu: {exc}]"

    return {"synthesis_output": output}
