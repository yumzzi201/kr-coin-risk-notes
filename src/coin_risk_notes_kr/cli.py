from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analyzer import analyze_project


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("Input JSON must be an object.")
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Korean educational crypto project risk checklist CLI. Not financial advice."
    )
    parser.add_argument("--input", "-i", required=True, help="Path to a project JSON file")
    parser.add_argument("--output", "-o", help="Optional path to write JSON result")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    project = _load_json(Path(args.input))
    result = analyze_project(project)
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
