#!/usr/bin/env python3
"""
Run retrieval evaluation on a golden set.

Usage:
    python scripts/run_eval.py --golden tests/fixtures/golden_minimal.json --k 10
"""

import argparse
import json
import sys
from pathlib import Path

# Make src importable when running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lex_qdrant_hybrid.evaluation.harness import load_golden, run_eval


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", required=True, help="Path to golden JSON")
    parser.add_argument("--k", type=int, default=10)
    args = parser.parse_args()

    golden = load_golden(args.golden)
    metrics = run_eval(golden, k=args.k)

    print(json.dumps(metrics, indent=2))
    # In real impl: sys.exit(0 only if metrics above threshold)


if __name__ == "__main__":
    main()