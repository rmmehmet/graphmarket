MAX_RETRIES = 2


def run(state: dict) -> dict:
    """Trend Research 'search_tool' sonuçlarını, Sales Insight retrieval citation'larını
    aynı 'evidence_count' alanı üzerinden değerlendirir.
    """
    evidence_count = state.get("evidence_count", 0)
    retry_count = state.get("retry_count", 0)

    if evidence_count >= 1:
        return {"verified": True}

    if retry_count >= MAX_RETRIES:
        return {"verified": True, "error": "yetersiz kanıtla tamamlandı (max retry)"}

    return {"verified": False, "retry_count": retry_count + 1}
