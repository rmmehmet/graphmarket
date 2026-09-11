from datetime import datetime, timezone
from pathlib import Path

from app.db.neo4j import get_session

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations_neo4j"


def _applied_versions(session) -> set[str]:
    result = session.run("MATCH (s:SchemaVersion) RETURN s.version AS version")
    return {record["version"] for record in result}


def run_migrations() -> list[str]:
    applied_now = []
    with get_session() as session:
        already_applied = _applied_versions(session)
        for path in sorted(MIGRATIONS_DIR.glob("*.cypher")):
            version = path.name
            if version in already_applied:
                continue
            statements = [s.strip() for s in path.read_text(encoding="utf-8").split(";") if s.strip()]
            for statement in statements:
                session.run(statement)
            session.run(
                "CREATE (s:SchemaVersion {version: $version, applied_at: $applied_at})",
                version=version,
                applied_at=datetime.now(timezone.utc).isoformat(),
            )
            applied_now.append(version)
    return applied_now


if __name__ == "__main__":
    applied = run_migrations()
    if applied:
        print("uygulanan migration'lar:", ", ".join(applied))
    else:
        print("uygulanacak yeni migration yok")
