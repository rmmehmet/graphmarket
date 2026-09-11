MAX_RETRIES = 2


def run(state: dict) -> dict:
    extracted = state.get("extracted", {})
    source_count = extracted.get("source_count", 0)
    retry_count = state.get("retry_count", 0)

    if source_count >= 1:
        return {"verified": True}

    if retry_count >= MAX_RETRIES:
        return {"verified": True, "error": "yetersiz kanıtla tamamlandı (max retry)"}

    return {"verified": False, "retry_count": retry_count + 1}
