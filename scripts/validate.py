#!/usr/bin/env python3
"""Validate the standalone product-prover package with only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"^\s*version:\s*([0-9]+\.[0-9]+\.[0-9]+-standalone)\s*$", re.M)


def fail(message: str) -> None:
    raise AssertionError(message)


def read(relative: Path | str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing required file: {relative}")
    return path.read_text(encoding="utf-8")


def version_from(text: str, source: str) -> str:
    match = VERSION_RE.search(text)
    if not match:
        fail(f"{source} carries no semantic standalone version")
    return match.group(1)


def validate_package() -> str:
    skill = read("SKILL.md")
    lenses = read("reference/stress-lenses.md")
    readme = read("README.md")
    response = read("examples/sample-response.md")
    rubric = json.loads(read("evals/sample-spec-rubric.json"))

    version = version_from(skill, "SKILL.md")
    if version not in readme:
        fail("README.md and SKILL.md disagree on the standalone version")
    if rubric.get("edition") != version:
        fail("the sample rubric does not name the current standalone version")

    flat_skill = " ".join(skill.split())
    flat_lenses = " ".join(lenses.split())
    for needle in (
        "under 1,500 words",
        "read-only by default",
        "highest-impact findings",
        "one-line index of every remaining finding",
    ):
        if needle not in flat_skill:
            fail(f"SKILL.md lost the compact response contract: {needle}")

    if "derive a working surface inventory" not in flat_skill or "label it review-derived" not in flat_skill:
        fail("SKILL.md no longer derives a surface inventory when the registry is absent")
    if "missing maintained registry never turns" not in flat_lenses:
        fail("the policy sweep can silently become N/A when a registry is absent")

    for forbidden in ("SPEC INV-", "[INV-", "base rule "):
        if forbidden in skill or forbidden in lenses:
            fail(f"public method files leaked an internal rule code: {forbidden}")

    max_words = rubric["acceptance"]["max_conversation_words"]
    response_words = len(response.split())
    if response_words > max_words:
        fail(f"sample response has {response_words} words; budget is {max_words}")
    if len(rubric.get("critical_findings", [])) < 6:
        fail("sample rubric needs at least six critical finding classes")
    if len(rubric.get("must_not_claim", [])) < 2:
        fail("sample rubric needs negative controls against invented claims")

    workflow = read(".github/workflows/validate.yml")
    if "scripts/validate.py" not in workflow:
        fail("standalone CI does not run this validator")
    return version


def main() -> int:
    try:
        version = validate_package()
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"product-prover standalone: FAIL — {exc}", file=sys.stderr)
        return 1
    print(f"product-prover standalone: OK — {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
