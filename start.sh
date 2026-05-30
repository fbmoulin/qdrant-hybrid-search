#!/usr/bin/env bash
# =============================================================================
# Qdrant Hybrid Search Project - One-Command Launcher
# Grok Build Terminal Factory Edition
# =============================================================================

set -e

echo "🚀 Qdrant Hybrid Search Factory Starting..."
echo ""

# Prerequisites check
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not found in PATH."
    echo "   Please install Docker Desktop or Docker Engine first."
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon is not running or not accessible."
    echo "   Please start Docker Desktop / Docker service."
    exit 1
fi

# 1. Start Qdrant (if not already running)
if ! docker ps | grep -q hybrid_qdrant; then
    echo "📦 Starting Qdrant via Docker Compose..."
    docker compose -f docker/docker-compose.yml up -d
    echo "⏳ Waiting for Qdrant to become healthy..."
    sleep 4
else
    echo "✅ Qdrant already running"
fi

# 2. Create/ensure the hybrid collection
echo ""
echo "🧠 Ensuring hybrid collection (dense + sparse)..."
python -c "
import sys
sys.path.insert(0, 'src')
from lex_qdrant_hybrid.collection_manager import CollectionManager
mgr = CollectionManager()
created = mgr.ensure_collection(dense_dim=384, sparse=True)  # 384 for all-MiniLM-L6-v2
print('Collection ready:', created)
"

# 3. Install minimal runtime deps if needed (fastembed for demo embeddings)
echo ""
echo "📦 Ensuring demo dependencies (fastembed for CPU hybrid embeddings)..."
pip install --quiet fastembed qdrant-client fastapi uvicorn pydantic python-dotenv 2>/dev/null || true

# 4. Start the FastAPI factory server
echo ""
echo "🔥 Starting FastAPI on http://localhost:8000"
echo "   Swagger UI: http://localhost:8000/docs"
echo ""
echo "💡 Tip: Before merging changes, run the hardened audit:"
echo "   ./scripts/run_full_audit.sh --full"
echo ""
echo "Press Ctrl+C to stop."
echo ""

exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload