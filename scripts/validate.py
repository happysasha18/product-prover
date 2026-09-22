#!/usr/bin/env python3
"""Validate the product-prover package with only the Python standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"^\s*version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.M)


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
        fail(f"{source} carries no semantic version")
    return match.group(1)


def validate_package() -> str:
    skill = read("SKILL.md")
    lenses = read("reference/stress-lenses.md")
    witnesses = read("reference/behavioral-witnesses.md")
    read("reference/code-lenses.md")
    read("reference/review-modes.md")
    read("reference/architecture-lens.md")
    read("reference/glossary-terms.md")
    readme = read("README.md")
    response = read("examples/sample-response.md")
    rubric = json.loads(read("evals/sample-spec-rubric.json"))
    witness_rubric = json.loads(read("examples/parcel-locker-witness-eval/rubric.json"))
    for fixture in ("flawed-spec.md", "fixed-spec.md", "ordered-control.md"):
        read(f"examples/parcel-locker-witness-eval/{fixture}")

    version = version_from(skill, "SKILL.md")
    if version not in readme:
        fail("README.md and SKILL.md disagree on the version")
    if rubric.get("version") != version:
        fail("the sample rubric does not name the current version")
    if witness_rubric.get("version") != version:
        fail("the behavioral witness rubric does not name the current version")
    positives = witness_rubric.get("flawed_spec_expected")
    if (
        not isinstance(positives, list)
        or len(positives) < 5
        or any(not isinstance(item, str) or not item.strip() for item in positives)
    ):
        fail("the behavioral witness fixture must exercise all four forms and distinct repairs")
    fixed_negatives = witness_rubric.get("fixed_spec_must_not_report")
    if (
        not isinstance(fixed_negatives, list)
        or len(fixed_negatives) < 4
        or any(not isinstance(item, str) or not item.strip() for item in fixed_negatives)
    ):
        fail("the repaired behavioral witness fixture needs explicit negative controls")
    ordered_negatives = witness_rubric.get("ordered_control_must_not_report")
    if (
        not isinstance(ordered_negatives, list)
        or len(ordered_negatives) < 2
        or any(not isinstance(item, str) or not item.strip() for item in ordered_negatives)
    ):
        fail("the behavioral witness fixture needs negative controls for intentional ordering")

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

    flat_witnesses = " ".join(witnesses.split())
    for needle in (
        "Replay or order witness",
        "Rule-selection witness",
        "Boundary-promise witness",
        "Progress witness",
        "does not create a second finding",
    ):
        if needle not in flat_witnesses:
            fail(f"behavioral witness procedure lost a required guard: {needle}")
    if "every reference file loaded during the pass" not in flat_skill:
        fail("the review record no longer fingerprints every loaded reference")

    for forbidden in ("SPEC INV-", "[INV-", "base rule "):
        if forbidden in skill or forbidden in lenses or forbidden in witnesses:
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
        fail("CI does not run this validator")
    return version


def main() -> int:
    try:
        version = validate_package()
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"product-prover: FAIL — {exc}", file=sys.stderr)
        return 1
    print(f"product-prover: OK — {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
