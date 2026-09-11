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

**Paylaşılan API client:** `packages/api-client` — tüm servis fonksiyonları (`authService`, `productsService`, ... ) burada; hem `frontend` hem `mobile` bunu npm workspace olarak kullanır. `configureApiClient({ baseURL, authStore })` ile host uygulama kendi token depolamasını (web: Zustand+localStorage, mobil: AsyncStorage) bağlar.

**Mobil (React Native / Expo):** `mobile/` — aynı `@satgit/api-client`'i kullanan Login/Register/Panel/Ürünler/Ajan ekranları.

```
cd mobile
npm run web      # tarayıcıda dene (react-native-web)
npm run android  # Android emülatör/cihaz (API_BASE_URL = 10.0.2.2, mobile/src/api.js'de)
npm run ios      # iOS simülatör (macOS gerekir)
```

Repo kökünde npm workspaces var (`frontend`, `packages/api-client`, `mobile`) — `npm install` kökte çalıştırılır.

Docker Compose ve prod kurulumu Faz 12'ye bırakıldı.
