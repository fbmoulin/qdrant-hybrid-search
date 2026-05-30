"""
Basic smoke tests for the hybrid service (modeled on vector-store-stj tests).
"""

import pytest


class TestHybridAPI:
    def test_health(self, client, api_prefix):
        resp = client.get(f"{api_prefix}/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "qdrant_url" in data

    def test_search_returns_200(self, client, api_prefix):
        """
        The service is designed for pre-computed vectors (n8n, agents, other embedders).
        Sending only a text query (no vectors) is valid HTTP but returns success=False
        with guidance — this is the intended behavior.
        """
        resp = client.post(
            f"{api_prefix}/search",
            json={
                "query": "capitalização de juros",
                "dense_vector": [0.01] * 8,
                "sparse_vector": {"indices": [1, 42], "values": [0.8, 0.3]},
                "top_k": 3
            }
        )
        assert resp.status_code == 200
        data = resp.json()
        # With vectors the call reaches the searcher (envelope is always returned)
        assert "success" in data
        assert "request_id" in data
        assert "execution_time_ms" in data

    def test_search_response_structure(self, client, api_prefix):
        """Response always contains the standard envelope fields."""
        response = client.post(
            f"{api_prefix}/search",
            json={
                "dense_vector": [0.0] * 4,
                "sparse_vector": {"indices": [0], "values": [1.0]}
            }
        )
        data = response.json()

        assert "success" in data
        assert "request_id" in data
        assert "query" in data
        assert "execution_time_ms" in data
        assert "total_results" in data
        assert "results" in data