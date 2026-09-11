# Prod'a Hazırlık — Faz 12

## Docker Compose

`docker-compose.yml` (repo kökü) bağımsız bir prod-benzeri stack tanımlar: Postgres,
Redis, Neo4j, Milvus (etcd+minio+standalone), backend, celery worker, frontend (nginx).

**Önemli:** Faz 0-11'de yerelde elle kurulan dev servisleriyle (`satgit-redis`,
`satgit-neo4j`, `milvus-standalone`, native Postgres 18) aynı anda çalıştırılmak üzere
tasarlanmadı — portlar kasıtlı olarak farklı seçildi (bkz. `.env.example`). Kullanmadan
önce:

```
cp .env.example .env   # değerleri doldurun
docker compose up -d --build
```

Backend container'ı başlarken `alembic upgrade head` otomatik çalışır.

## Yönetilen servislere geçiş değerlendirmesi

Şu an her şey kendi barındırılan (self-hosted) container/servis olarak çalışıyor. Ölçek
büyüdükçe aşağıdaki geçişler değerlendirilebilir:

| Bileşen | Şu an | Yönetilen alternatif | Ne zaman geçilir |
|---|---|---|---|
| Neo4j | Docker container, tek node | **Neo4j Aura** (managed) | Yüksek erişilebilirlik/otomatik yedekleme gerektiğinde, veya ops yükü (patching, disk büyütme) manuel yönetilemez hale geldiğinde. Aura Free tier küçük graph'lar için MVP sonrası bile yeterli olabilir. |
| Milvus | Docker Compose (etcd+minio+standalone) | **Zilliz Cloud** (Milvus'un yönetilen hali) | Vektör sayısı/QPS arttığında, ya da etcd/minio/milvus üçlüsünü kendi başına ölçeklemek (sharding, replika) ops maliyeti yaratmaya başladığında. |
| PostgreSQL | Docker container (ya da yerelde native) | RDS / Cloud SQL / Neon / Supabase | Prod'a çıkarken hemen — otomatik yedekleme ve point-in-time recovery kendi container'ında yok. |
| Redis | Docker container | Upstash / ElastiCache | Celery kuyruğu kritikleştiğinde (kaybolan job = kaybolan iş) — yönetilen Redis'in kalıcılık/failover garantisi devreye girer. |

**Öneri sırası:** Postgres ve Redis'i ilk prod dağıtımında hemen yönetilen bir servise
taşımak (veri kaybı riski en yüksek, geçiş maliyeti en düşük); Neo4j Aura ve Zilliz
Cloud'u trafik/veri büyüklüğü gerçek bir ops yükü yarattığında değerlendirmek — MVP
ölçeğinde self-hosted container'lar hem daha ucuz hem de bu projede zaten çalışır
durumda.

## Frontend prod build & env değişkenleri

- `frontend/.env.example` → `VITE_API_BASE_URL`, `VITE_SENTRY_DSN`.
- `docker-compose.yml`'de frontend imajı build-time'da `VITE_API_BASE_URL`'i alır (Vite
  değişkenleri build'e gömülür, runtime'da değiştirilemez — imaj her ortam için ayrı
  build edilmeli ya da bir reverse proxy ile ortama özgü `env.js` enjekte edilmeli).
- `ErrorBoundary` (`frontend/src/components/ErrorBoundary.jsx`) tüm uygulamayı sarar,
  `@sentry/react`'in `ErrorBoundary`'sini kullanır — `VITE_SENTRY_DSN` boşken sessizce
  hiçbir şey göndermez (Faz 6/8/10'daki "anahtar yoksa no-op" deseniyle tutarlı).

## Doğrulanan

- `backend/Dockerfile` — gerçek `docker build` ile derlendi, container içinde
  `pymilvus`/`pkg_resources` ve `app.main` import'u doğrulandı.
- `frontend/Dockerfile` — gerçek `docker build` ile derlendi (repo kökü context'i,
  `@satgit/api-client` workspace paketiyle), nginx SPA fallback (`/dashboard` gibi
  client-side route'lar 200 dönüyor) doğrulandı.
- `docker-compose.yml` — `docker compose config` ile syntax/interpolation doğrulandı.
  Not: `node:22-alpine` üzerinde Vite'ın rolldown bağımlısı musl (Alpine) binary'sini
  bulamadığı için build stage `node:22-slim`'e (glibc) çevrildi; ayrıca Windows'ta
  üretilen `package-lock.json` platform-özel opsiyonel bağımlılıkları (rolldown'un
  win32 binary'si) kilitlediğinden Docker build'inde kopyalanmıyor — Linux için taze
  `npm install` çalıştırılıyor.
