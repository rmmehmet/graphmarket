import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.providers.router import get_provider
from app.core.security import decrypt_secret, encrypt_secret
from app.models.model_profile import ModelProfile

DEFAULT_PROFILES = {
    "planner": {"provider": "ollama", "model_name": "llama3.2"},
    "extraction": {"provider": "huggingface", "model_name": None},
    "synthesis": {"provider": "claude_subscription", "model_name": None},
    "verification": {"provider": "anthropic_api", "model_name": "claude-3-5-sonnet-20241022"},
}


def _to_out(node: str, provider: str, model_name: str | None, api_key_encrypted: str | None) -> dict:
    return {
        "node": node,
        "provider": provider,
        "model_name": model_name,
        "has_api_key": api_key_encrypted is not None,
    }


def get_model_profiles(db: Session, team_id: str) -> list[dict]:
    rows = {
        row.node_name: row
        for row in db.scalars(select(ModelProfile).where(ModelProfile.team_id == team_id))
    }
    result = []
    for node, default in DEFAULT_PROFILES.items():
        row = rows.get(node)
        if row is not None:
            result.append(_to_out(node, row.provider, row.model_name, row.api_key_encrypted))
        else:
            result.append(_to_out(node, default["provider"], default["model_name"], None))
    return result


def upsert_model_profile(
    db: Session,
    team_id: str,
    node: str,
    provider: str,
    model_name: str | None,
    api_key: str | None,
) -> dict:
    row = db.scalar(
        select(ModelProfile).where(ModelProfile.team_id == team_id, ModelProfile.node_name == node)
    )
    api_key_encrypted = encrypt_secret(api_key) if api_key else (row.api_key_encrypted if row else None)

    if row is None:
        row = ModelProfile(
            team_id=team_id,
            node_name=node,
            provider=provider,
            model_name=model_name,
            api_key_encrypted=api_key_encrypted,
        )
        db.add(row)
    else:
        row.provider = provider
        row.model_name = model_name
        row.api_key_encrypted = api_key_encrypted

    db.commit()
    db.refresh(row)
    return _to_out(node, row.provider, row.model_name, row.api_key_encrypted)


def resolve_profile(db: Session, team_id: str, node: str) -> tuple[str, str | None, str | None]:
    row = db.scalar(
        select(ModelProfile).where(ModelProfile.team_id == team_id, ModelProfile.node_name == node)
    )
    if row is not None:
        api_key = decrypt_secret(row.api_key_encrypted) if row.api_key_encrypted else None
        return row.provider, row.model_name, api_key

    default = DEFAULT_PROFILES.get(node)
    if default is None:
        raise ValueError(f"unknown node: {node}")
    return default["provider"], default["model_name"], None


def test_model_profile(db: Session, team_id: str, node: str) -> dict:
    provider_name, model_name, api_key = resolve_profile(db, team_id, node)
    provider = get_provider(provider_name, model_name, api_key)

    start = time.perf_counter()
    try:
        provider.test_connection()
        return {"ok": True, "latency_ms": int((time.perf_counter() - start) * 1000), "error": None}
    except Exception as exc:
        return {
            "ok": False,
            "latency_ms": int((time.perf_counter() - start) * 1000),
            "error": str(exc),
        }
