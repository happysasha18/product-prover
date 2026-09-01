# Changelog

## Release history

This repository's own line:

- 1.6.1 · 2026-09-01 — the README is rewritten short. It ran to 243 lines and opened on the method
  rather than on what a reader gets, so a first-time reader met the internal vocabulary before the
  problem it solves. The new order is what you get, an example finding quoted from the sample run,
  how the logic works, who it fits, then usage and install last. Two sections move out of the README
  into their own pages: the fuller account of the method, the genre question, and what sits beside
  this pass are now in new `docs/how-it-works.md`, and the four known issues are now in new
  `docs/known-issues.md`, both linked from the README. The sample-response pointer named five
  findings where `examples/sample-response.md` carries ten, and now names ten. `README.md` is 70
  lines, down from 243. No wording of the method changed, and a review's behaviour — what it finds,
  in what order, in what format — is unchanged.
- 1.6.0 · 2026-08-31 — `SKILL.md` ran to 898 lines against skill-creator's guideline of roughly 500,
  even after the stress lenses and the code lenses were externalized. Three more sections move out,
  each one material a review reaches for only on a particular turn, never on every pass: the
  New-surface review's seven lenses and quantifier re-verify, the Feature-fit review's seven journey
  seams and second-sibling question, and the pre-merge gate's three parts and four blockers, all now
  in new `reference/review-modes.md`; the architecture lens's seven checks, armed only when Phase 0
  reads an architecture document, now in new `reference/architecture-lens.md`; and glossary mode's
  exact term definitions, reached only by a standalone glossary request, now in new
  `reference/glossary-terms.md`. The body keeps what every pass needs regardless of mode or input: the
  finding format, the phases, the mandatory sweeps' and class lens's home in Phase 3e, and a short
  pointer at each site naming when to open the new file. `scripts/validate.py` now checks all three
  new files exist, beside the two it already checked. `SKILL.md` is 734 lines, down from 898. No
  wording of the method changed, and a review's behaviour — what it finds, in what order, in what
  format — is unchanged.
- 1.5.0 · 2026-08-31 — the architecture lens has a place in the pipeline. Its seven checks were
  written inside Phase 0, whose stated job is the triage decision alone, so nothing said when they
  ran or what a finding from them looked like. They now run in Phase 3e beside the mandatory sweeps,
  which is where a lens run over every member of a class already lives, and one of the seven — every
  seam names what crosses it and which side owns the format — is the unwritten-seams sweep restated.
  Phase 0 keeps the routing: it arms the lens and names the paired requirements document the
  ownership check reads against. A finding from the lens takes the same four-part format every other
  finding takes, and each of the seven checks owes one verdict line — hit, clean, or N/A with its
  reason — standing beneath the class line, with the per-file node counts beneath the node-growth
  line. The seven checks themselves are unchanged, and so is every other phase, mode, sweep, and
  finding rule. A review of a document that is not an architecture document reads exactly as it did
  in 1.4.3.

  The merge gate's four blockers are now a list: an unmatched token, a red suite, a finding present
  on the new side and absent on the old side, and a meaning change nobody named. They were two
  sentences of prose with the fourth stranded, which the skill's own cognitive-load lens flags. All
  four blockers are unchanged. The same shape was swept and fixed in two more places: Phase 4's three
  shapes of leaked internal vocabulary, and glossary mode's three outputs for a single term.

  Known and pending: `SKILL.md` runs past the roughly 500-line guideline for a skill body even with
  two reference files externalized. Splitting it further belongs to its own pass.
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
