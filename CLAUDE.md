# Qdrant Hybrid Search Project - Claude Code Instructions

## Project Overview
This is the **Grok Build Terminal Factory** drop for production hybrid search (Dense + Sparse + RRF).

It is both:
- A ready-to-run demo (run `./start.sh`)
- A reusable library (`src/lex_qdrant_hybrid/`)

## Key Commands
- **One-command launch**: `./start.sh`
- **Swagger UI**: http://localhost:8000/docs
- **Ingest + Search demo**:
  ```bash
  curl -X POST http://localhost:8000/ingest -d '{"text": "Your document here", "metadata": {"category": "blog"}}'
  curl -X POST http://localhost:8000/search -d '{"query": "your question", "fusion": "rrf"}'
  ```

## Architecture
- `main.py` — Demo FastAPI factory surface (`/ingest`, `/search`)
- `hybrid_search.py` + `qdrant_setup.py` — Thin factory wrappers
- `src/lex_qdrant_hybrid/` — The real production library (use this in real projects)
- `docker/` — Qdrant + service compose

## Rules (Path-Scoped)
See `.claude/rules/` for:
- `qdrant-hybrid.md` — The most important file in this project
- `backend.md`
- `testing.md`

**Follow these rules when modifying anything in `src/`, `app/`, or the demo.**

## Important Decisions
- We use **named vectors** ("dense" + "sparse") — this is non-negotiable for true hybrid.
- Demo uses `fastembed` (CPU) for both dense and sparse so it "just works".
- Real production use should bring your own embedders (see the library).

## Common Gotchas
- You must run `./start.sh` (or at least create the collection) before ingesting.
- `fastembed` is required for the magic one-command demo.

## Next Level
This project is designed to be dropped into any RAG/agent system.
See `examples/` and the library docs in `src/`.

## Audit & Quality Gates
**Before merging any non-trivial change**, you **must** run the hardened audit:

```bash
./scripts/run_full_audit.sh --full     # Full suite (Testcontainers + real metrics)
# or
make audit-full
```

This runs:
- Unit + Factory tests
- Spec compliance verification (prefetch + RRF from the original hybrid spec)
- Real retrieval quality metrics (NDCG@10 / Recall@10 / MRR)
- Integration tests against a real Qdrant instance (via Testcontainers)

### CI Behavior
- A clean summary table is automatically posted on every PR.
- The `audit-gate` job is the single source of truth for merge decisions.
- Full reports are available as build artifacts.

**Making `audit-gate` a required check** (strongly recommended for this repo):
See the comments at the bottom of `.github/workflows/audit.yml` for exact branch protection instructions.

See `docs/specs/audit-hardening-v2.md` for the complete Audit Hardening v2 specification.