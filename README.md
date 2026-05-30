# Qdrant Hybrid Search Project — Grok Build Terminal Factory 🔥

** 🎥 YO BUILDERS! Welcome to the Grok Build Terminal Factory!**

Today we’re dropping the **complete, ready-to-execute Qdrant Hybrid Search Project**.

- ✅ FastAPI backend with real **hybrid search** (Dense + Sparse + RRF)
- ✅ Automatic Qdrant collection with both vector types + payload indexes
- ✅ Production `/search` + `/ingest` endpoints
- ✅ Full `CLAUDE.md` + path-scoped rules (ready for Claude Code)
- ✅ Docker Compose for local Qdrant
- ✅ One-command `start.sh`

**Everything lives here:**
```bash
/home/workdir/artifacts/qdrant-hybrid-search-project/
```

## Audit Status (CI Gate)

[![Audit](https://github.com/fbmoulin/qdrant-hybrid-search/actions/workflows/audit.yml/badge.svg)](https://github.com/fbmoulin/qdrant-hybrid-search/actions/workflows/audit.yml)

The hardened audit (Testcontainers + real retrieval metrics + spec compliance) runs on every PR. The `audit-gate` job is intended to be set as a **required status check** before merging.

## 3-Step Execution (Grok Build Terminal)

**Step 1: Enter the factory**
```bash
cd /home/workdir/artifacts/qdrant-hybrid-search-project
```

**Step 2: Make it executable & launch**
```bash
chmod +x start.sh
./start.sh
```

This will:
- Spin up Qdrant in Docker
- Create the hybrid collection
- Install dependencies
- Start FastAPI on `http://localhost:8000`

**Step 3: Test it instantly**
Open Swagger UI: http://localhost:8000/docs

Try these:
- `POST /ingest` → add sample documents (auto-embeds with fastembed!)
- `POST /search` → query with real hybrid power + filters

## Full Audit Suite (Production Gate)

This project ships with a **hardened, production-grade audit system** (detailed in `docs/specs/audit-hardening-v2.md`).

### Local Usage

```bash
# Fast checks only (unit + factory + spec compliance)
./scripts/run_full_audit.sh

# Full hardened audit (recommended before merging or releasing)
# → Uses Testcontainers for real Qdrant + runs retrieval quality metrics
./scripts/run_full_audit.sh --full

# Or via Make
make audit
make audit-full
```

The audit validates:
- Spec compliance (`prefetch` + RRF fusion from the original 2026 hybrid spec)
- Real retrieval quality (NDCG@10, Recall@10, MRR via `ranx`)
- Factory demo behavior (`/ingest` + `/search`)
- Integration tests with actual Qdrant instances

### CI Enforcement

On every PR and push to main, GitHub Actions runs the complete audit suite.

- A clean **summary table is automatically posted** as a comment on every PR.
- The full `audit-report.md` + `audit-report.json` are uploaded as build artifacts.
- The `audit-gate` job acts as the single required status check.

**To make the audit a hard requirement** (highly recommended):

1. Go to **Settings → Branches → Branch protection rules** for `main`
2. Enable **"Require status checks to pass before merging"**
3. Select `audit-gate` (and optionally `unit-and-spec`)
4. Enable **"Require branches to be up to date before merging"**

This ensures **no code** can be merged unless the full hardened audit (including real hybrid search quality metrics) passes.

---

**Below is the full professional library documentation:**

# lex-qdrant-hybrid (Library)

Production-grade **hybrid (dense + sparse) search** library + optional FastAPI microservice for Qdrant.

Implements the 2026 best practices from the authoritative spec (prefetch + RRF / DBSF / FormulaQuery, named vectors, payload indexing, quantization hooks, retrieval evaluation).

Designed as a reusable component for the KRATOS / Lex Intelligentia judicial AI ecosystem.

## Quick Start (SDK)

```python
from lex_qdrant_hybrid import CollectionManager, HybridSearcher, get_settings

settings = get_settings()

# 1. Ensure collection exists with proper hybrid config (named "dense" + "sparse")
mgr = CollectionManager(settings.qdrant_url, settings.collection)
mgr.ensure_collection(dense_dim=1024, sparse=True)

# 2. Search
searcher = HybridSearcher(settings.qdrant_url, settings.collection)
results = searcher.hybrid_search(
    query="capitalização de juros em contratos bancários",
    top_k=5,
    fusion="rrf",           # or "weighted_rrf", "dbsf", "formula"
    filters={"ramo_direito": "DIREITO_CIVIL"}
)
```

## Quick Start (HTTP Service)

```bash
docker compose -f docker/docker-compose.yml up --build -d
curl -X POST http://localhost:8080/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "danos morais negativação indevida", "fusion": "rrf", "top_k": 5}'
```

## Key Features

- True hybrid: dense (E5 / OpenAI / custom) + sparse (BM25 via fastembed primary)
- All recommended fusion methods (RRF k=60, weighted, DBSF, FormulaQuery with recency/popularity decay)
- Declarative collection lifecycle (CollectionManager)
- Pluggable embedders + reranker hook
- First-class retrieval evaluation harness (NDCG@K, Recall, MRR)
- Judicial-friendly response shapes + n8n AI Agent tool format (inspired by vector-store-stj)
- structlog throughout
- GPU-ready Docker images
- Self-contained `.claude/` rules (the project was built following its own rules)

## Installation

```bash
# Core (SDK only)
pip install lex-qdrant-hybrid

# With FastAPI service + dev tools
pip install "lex-qdrant-hybrid[dev]"

# GPU embedders
pip install "lex-qdrant-hybrid[gpu]"

# Sparse + evaluation
pip install "lex-qdrant-hybrid[sparse,eval]"
```

## Project Layout

```
src/lex_qdrant_hybrid/     # importable library (the real product)
app/                       # optional FastAPI service
docker/                    # Dockerfiles + compose (cpu + gpu profiles)
tests/
evaluation/                # golden dataset harness + metrics
scripts/                   # create_collection, run_eval, etc.
examples/                  # n8n, STJ migration, etc.
.claude/                   # path-scoped rules + CLAUDE.md (eat our own dogfood)
```

## Reusing in Existing Projects

See `examples/migrate_stj_to_hybrid.py` for a drop-in adapter that lets the existing STJ vector-store use this HybridSearcher as its backend.

## Evaluation

```bash
python scripts/run_eval.py --golden tests/fixtures/golden_minimal.json --k 10
```

A small synthetic golden set is included so CI can always run a smoke eval. Real judicial golden sets live outside the repo (or in a private `golden/` volume).

## Status

Early alpha. Core hybrid search + collection manager are functional. FastAPI surface and full eval harness are being completed in the initial implementation wave.

## Credits & Sources

- Hybrid strategies: the detailed 2026 guide + code examples provided in the originating conversation (prompt_0.txt).
- Dense embedder patterns + judicial schemas: extracted and generalized from `projetos-2026/vector-store-stj/`.
- MCP Qdrant patterns: `kratos-master-lex/services/mcp-qdrant/`.

Built following the CLAUDE.md + path-scoped rules best practices documented in the same conversation.