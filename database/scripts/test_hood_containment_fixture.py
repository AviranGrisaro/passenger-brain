#!/usr/bin/env python3
"""
Asserts database/scripts/validate_dataset.py's resolve_hood() against the
shared cross-language fixture (database/data/fixtures/hood-containment-cases.json),
per hood-dataset/TRD.md sec 11 B1. No test framework dependency (this repo's
Python scripts are stdlib-only, database/README.md) -- run directly:

    python3 database/scripts/test_hood_containment_fixture.py

T-043's SQL hood_for_point() must be asserted against the same fixture file
in its own build; this script only covers the offline/Python side
(T-040/T-042).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_dataset import load_hood_source, resolve_hood  # noqa: E402

FIXTURE = Path(__file__).resolve().parent.parent / "data" / "fixtures" / "hood-containment-cases.json"


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    source_path = Path(__file__).resolve().parent.parent / fixture["sourceFile"].split("database/", 1)[-1]
    # sourceFile is repo-relative from `database/`; resolve against this file's
    # own database/ ancestor rather than assuming a cwd.
    source_path = Path(__file__).resolve().parents[1] / "data" / "hoods-tel-aviv.source.json"
    dataset = load_hood_source(source_path)

    failures = []
    for case in fixture["cases"]:
        got = resolve_hood(dataset, case["lng"], case["lat"])
        expected = case["expectedHoodId"]
        status = "PASS" if got == expected else "FAIL"
        if status == "FAIL":
            failures.append(case)
        print(f"[{status}] {case['description']!r}: expected={expected!r} got={got!r}")

    print(f"\n{len(fixture['cases']) - len(failures)}/{len(fixture['cases'])} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
