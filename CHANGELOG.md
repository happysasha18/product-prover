# Changelog

## Release history

This repository's own line:

- 1.4.0 · 2026-08-26 — code mode: a fourth door, for a source directory, a family of sibling scripts,
  or a diff with no accompanying document. Phase 0 now routes a document-less input here instead of
  `WRONG_ARTIFACT`. It carries three capabilities from the document pass, adapted to code's own
  ground: class-based defect analysis, sibling-defect search (the mechanical techniques that answer
  the class lens's "does the same mistake live elsewhere" question in code), and closed-set
  completeness. It leaves out what needs a document to check against: declared cross-cutting laws,
  lifecycle sweeps, provisional defaults, three-source disagreement. New file
  `reference/code-lenses.md` carries the procedure; `SKILL.md` gained a "Code mode" section, a Phase 0
  branch, an exception in "Work that belongs elsewhere", and a triggering description. No document-mode
  text changed beyond that.
- 1.3.1 · 2026-08-19 — `scripts/validate.py` still demanded the pre-canon `-standalone` version
  suffix that release 1.3.0 dropped on purpose, so CI read red from 2026-08-13 on; the validator now
  accepts a plain semantic version, and the leftover "edition"/"mirror" wording from before this
  repository became the canon is cleaned out of the workflow name, the sample rubric, PROVENANCE.md,
  and SKILL.md's own footer.
- 1.3.0 · 2026-08-13 — the repository becomes the canon: machine-name mode aliases for pipeline
  callers, the closing summary names the version that ran, and the mirror language leaves the README
- 1.2.0 · 2026-08-13 — standalone reviews made compact and releasable
- 1.1.0 · 2026-08-13 — the compact conversation contract, the sample response, and the versioned
  acceptance rubric
- 1.0.0 · 2026-08-05 — first standalone release, lifted from the pack; the stress lenses split into
  `reference/stress-lenses.md`

The skill's earlier growth happened inside the [live-spec](https://github.com/happysasha18/live-spec)
pack, through pack release 4.3.0. One line per pack release lives in the pack's
[JOURNAL.md](https://github.com/happysasha18/live-spec/blob/main/JOURNAL.md).
