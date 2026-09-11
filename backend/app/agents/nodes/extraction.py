import json
import re

from app.agents.providers.router import get_provider
from app.services.job_service import db_session
from app.services.settings_service import resolve_profile


def run(state: dict) -> dict:
    if "message_text" in state:
        return _run_messenger(state)
    return _run_trend(state)


def _get_extraction_provider(team_id: str):
    with db_session() as db:
        provider_name, model_name, api_key = resolve_profile(db, team_id, "extraction")
    return get_provider(provider_name, model_name, api_key)


def _run_trend(state: dict) -> dict:
    team_id = state["team_id"]
    search_results = state.get("search_results", [])
    combined_text = "\n".join(r["snippet"] for r in search_results)

    provider = _get_extraction_provider(team_id)
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
        },
        "evidence_count": len(search_results),
        "synthesis_prompt": (
            f"'{state['category']}' kategorisi için şu çıkarım özetine dayanarak kısa "
            f"bir pazar trend raporu yaz (3-4 madde, Türkçe):\n\n{summary}"
        ),
    }


def _parse_json_loosely(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("model çıktısında JSON nesnesi bulunamadı")
    return json.loads(match.group(0))


def _run_messenger(state: dict) -> dict:
    team_id = state["team_id"]
    message_text = state["message_text"]

    provider = _get_extraction_provider(team_id)
    prompt = (
        "Aşağıdaki müşteri mesajından ürün adını, bahsedilen fiyatı (varsa, sayı olarak) ve "
        "duygu durumunu (pozitif/negatif/nötr) çıkar. SADECE şu formatta JSON döndür: "
        '{"product_hint": "..." veya null, "price": sayı veya null, "sentiment": "pozitif|negatif|nötr"}'
        f"\n\nMesaj: {message_text}"
    )
    try:
        raw = provider.complete(prompt)
        extracted = _parse_json_loosely(raw)
    except Exception as exc:
        extracted = {"product_hint": None, "price": None, "sentiment": "nötr", "error": str(exc)}

    return {"extracted": extracted}
