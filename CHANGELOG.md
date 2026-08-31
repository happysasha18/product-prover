# Changelog

## Release history

This repository's own line:

- 1.4.3 · 2026-08-31 — code mode is described as two lenses, not three: sibling-defect search was
  already written as "the mechanical half of that same lens", not a peer capability, so the heading
  and enumeration in `reference/code-lenses.md`, the "carries three of the document pass's
  capabilities" sentence in `SKILL.md`'s Code mode section, and the matching sentence in the README
  now count two, with sibling-defect search folded into the class lens as its mechanical half. The
  review logic is unchanged.
- 1.4.2 · 2026-08-28 — the frontmatter description in `SKILL.md` is shortened, for reliable discovery
  routing. The README hero is split into two short paragraphs, for readability. The review logic of
  both document mode and Code mode is unchanged.
- 1.4.1 · 2026-08-28 — the README now positions Code mode clearly as a limited code-only mode, next
  to the spec-review it primarily does: a top-line sentence names both, an ordinary-text usage
  example covers a code-only prompt, the Code mode section links `reference/code-lenses.md` and
  states the boundary — no replacement for a full code review, no check against a spec that doesn't
  exist — and Known issues no longer calls Code mode one of "the two narrow modes". `scripts/validate.py`
  now checks that `reference/code-lenses.md` exists and is readable, since `SKILL.md` opens it in
  Code mode. The review logic of both document mode and Code mode is unchanged.
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
