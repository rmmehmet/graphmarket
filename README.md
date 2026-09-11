# SatGit

Küçük satıcılar için agentic GraphRAG pazar zekası asistanı. Mimari ve tasarım kararları için `docs/PUSULA_MIMARI.md` ve `docs/PUSULA_TASARIM_SISTEMI.md`.

## Faz 0 — Kurulum durumu

**Veritabanları (her biri kendi `satgit` adıyla, diğer projelerden ayrı):**
- PostgreSQL 18 (yerel servis, port 5432) — database `satgit`
- Neo4j 5 (Docker container `satgit-neo4j`, port 7687/7474) — default database `satgit`, kullanıcı `neo4j`
- Milvus 2.3.5 (Docker container `milvus-standalone`, port 19530) — database `satgit`
- Redis 7 (Docker container `satgit-redis`, port **6390** — 6379 host'ta çakışabileceği için farklı seçildi)

**Backend:** `backend/` — FastAPI + venv (`backend/.venv`), Alembic yapılandırıldı (`alembic/`), ilk migration `0001_init`.

```
cd backend
./.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

**Frontend:** `frontend/` — Vite + React, routing/AppShell iskeleti, `tokens.css` uygulandı.

```
cd frontend
npm run dev
```

Git henüz başlatılmadı (kullanıcı isteği). Docker Compose ve prod kurulumu Faz 12'ye bırakıldı.
