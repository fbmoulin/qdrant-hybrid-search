#!/usr/bin/env python3
"""
Declarative hybrid collection creator (uses CollectionManager).

Example:
    python scripts/create_hybrid_collection.py --name stj_jurisprudencia_hybrid --dense-dim 1024 --sparse
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lex_qdrant_hybrid.collection_manager import CollectionManager


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--dense-dim", type=int, default=1024)
    parser.add_argument("--sparse", action="store_true")
    args = parser.parse_args()

    mgr = CollectionManager(collection=args.name)
    ok = mgr.ensure_collection(dense_dim=args.dense_dim, sparse=args.sparse)
    print(f"Collection {args.name} ensured: {ok}")


if __name__ == "__main__":
    main()