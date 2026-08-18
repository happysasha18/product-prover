# Changelog

## Release history

This repository's own line:

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
