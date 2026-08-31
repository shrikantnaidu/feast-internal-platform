# Feast — Feature Store Docker Stack

On-premise Feast feature store deployment featuring low-latency online serving with Redis, historical feature retrieval with PostgreSQL, centralized SQL registry, and the Feast Web UI.

---

## 🏗 Architecture

```
feast/
├── postgres:16          # SQL Registry (metadata) + Offline Feature Store
├── redis:7.2-bookworm   # Online Store for sub-millisecond feature lookup
├── feast                # Feast Feature Server (FastAPI REST endpoint on Port 6566)
├── feast-ui             # Feast Web UI for exploring entities & features (Port 8888)
└── feast-init           # One-shot container running `feast apply` to sync definitions
```

---

## 📁 Directory Structure

```
feast/
├── .env.example         # Safe configuration template
├── .env                 # Local secrets and exposed port configuration (not committed)
├── Dockerfile           # Python 3.11-slim + Feast with Postgres, Redis, and gRPC extras
├── docker-compose.yml   # Multi-service container orchestration definition
├── requirements.txt     # Feast package requirements (feast[postgres,redis], grpcio, etc.)
└── feature_repo/        # Feast feature definitions repository
    └── feature_store.yaml.template # Runtime-rendered PostgreSQL + Redis configuration
```

---

## 🚀 Quick Start

### 1. Configure Environment (`.env`)

Copy `.env.example` to `.env`, then replace both `change-me` values with strong secrets.

```env
POSTGRES_USER=feast
POSTGRES_PASSWORD=change-me
POSTGRES_DB=feast
REDIS_PASSWORD=change-me
FEAST_PORT=6566
FEAST_UI_PORT=8888
```

### 2. Build & Start

```bash
# Build custom Feast image
docker compose build

# Start the stack
docker compose up -d
```

### 3. Verify Health

```bash
# Check container status
docker compose ps -a

# Test Feature Server health
curl http://localhost:6566/health

# Test Feast UI
curl -I http://localhost:8888
```

- **Feast Feature Server API**: [http://localhost:6566](http://localhost:6566)
- **Feast Web UI**: [http://localhost:8888](http://localhost:8888)

The default Compose configuration binds both endpoints to localhost. The container entrypoint renders `feature_store.yaml` from runtime environment variables before running `feast-init`, `feast`, or `feast-ui`.

---

## ⚙️ Adding & Applying Feature Definitions

1. Define your entities, data sources, and feature views in Python files under [feature_repo/](./feature_repo/).
2. Apply changes to the central SQL registry and online store:
   ```bash
   # Rebuild first so the image contains the latest definitions
   docker compose build

   # Re-run the one-shot init container to apply updates
   docker compose run --rm feast-init
   ```
3. Restart or reload the feature server if needed:
   ```bash
   docker compose restart feast
   ```

---

## 🔌 Retrieving Online Features (Inference Example)

```python
import requests

# Query the online feature server via HTTP REST API
response = requests.post(
    "http://localhost:6566/get-online-features",
    json={
        "features": ["user_features:daily_transactions", "user_features:risk_score"],
        "entities": {"user_id": [1001, 1002]}
    }
)
print(response.json())
```

---

## 🛠 Useful Commands

| Task | Command |
|---|---|
| Stop stack | `docker compose down` |
| View feature server logs | `docker compose logs -f feast` |
| View UI logs | `docker compose logs -f feast-ui` |
| Run manual `feast apply` | `docker compose run --rm feast-init` |
| Tear down + wipe storage | `docker compose down -v` *(deletes database and Redis volumes)* |
