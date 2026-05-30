"""
Qdrant Hybrid Collection Setup
==============================

Factory helper. Creates the proper hybrid collection (dense + sparse + indexes).
"""

from __future__ import annotations

from src.lex_qdrant_hybrid.collection_manager import CollectionManager

__all__ = ["CollectionManager"]


def create_hybrid_collection(name: str = "hybrid_documents", dense_dim: int = 384) -> bool:
    """Convenience function for the factory experience."""
    mgr = CollectionManager(collection=name)
    return mgr.ensure_collection(dense_dim=dense_dim, sparse=True)