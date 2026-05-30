"""
Hybrid Search Core (RRF Magic)
==============================

This is the extracted "hero" module from the Grok Build Terminal Factory drop.
It uses the production-grade logic from src/lex_qdrant_hybrid under the hood.
"""

from __future__ import annotations

from src.lex_qdrant_hybrid.hybrid_searcher import HybridSearcher, HybridResult, Fusion

__all__ = ["HybridSearcher", "HybridResult", "Fusion"]