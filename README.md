**product-prover** — one skill from the [live-spec pack](https://github.com/happysasha18/live-spec), installable on its own. Read-only mirror: do not open PRs here; changes land in the pack and are synced by scripts/sync-mirrors.sh.

# product-prover

**A senior-architect review of your product spec, through the lens of [formal verification](https://en.wikipedia.org/wiki/Formal_verification). A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a PRD, feature spec, HLD, or design proposal. It reads the document the way a principal architect would: a short verdict, the structural model it extracted, the gaps that matter, and what to fix before you build.

---

## Why

A spec passes review because reviewers can only catch errors in the language the document is written in. A missing rollback, a state with no exit, an operation that isn't atomic — these have no words on the page to argue with, so nobody argues.

That used to be survivable, because a human had to read the document before building against it, and a person building against a hole produces friction: a question in grooming, a spike, an argument. An agent generating from the same document produces no friction at all. It fills the hole with a plausible default and keeps going. Then the tests get derived from the same document, so they say nothing about the missing property either.

Green suite. Shipped gap. The review has to happen on the document, before anything is generated from it.

---

## What a finding looks like

Findings arrive in operational terms, each one traced to a quote in your document. Illustrative:

> **A failed update can be silently overwritten by the next one**
>
> *Spec §4.2:* "If the update fails, the tenant enters `Failed to Update`." The document defines no transition out of that state, and §4.3 allows a new update from any state.
>
> **Consequence:** a tenant whose update failed at 14:02 receives a second update at 14:05 that succeeds. The tenant now reads `Updated`. The billing service that consumed the first update never learns it was lost, and no operator sees an error — the failure is gone from the record.
>
> **Fix:** state the exit from `Failed to Update` — retry, revert to last consistent state, or a hard stop that alerts an operator — and state whether a new update is accepted before that exit is taken.
>
> `defect · unresolved-failure-state (liveness)`

The formal vocabulary appears only in that last tag. The framework stays private; you get the finding.

Every finding is one of two kinds, and the tag says which. A **defect** — a violated invariant, a false claim, or a missing required answer — blocks the build: it is folded into the spec before you ship. A **recommendation** — a consistency or quality gain with nothing broken — queues for a taste call, and you decide.

---

## The rule it won't break

> Never produce a finding the reader can't trace back to the document.

Every finding quotes its source and pins the location. Every consequence is concrete — who is affected, what triggers it, what breaks, what they see — not "this could be a problem." Every fix names a specific artifact or decision; the vague verbs (`define`, `ensure`, `handle`, `consider`) are banned. When the document is too vague to support a concrete consequence, it says so plainly instead of inventing one.

An adversarial reviewer that produces plausible fiction is worse than no reviewer.

The verdict tracks production impact, not formal purity: the same atomicity gap is a recommendation for a manual quarterly job and a defect for an automated path that runs a thousand times a day. The reasoning lives in the finding, not in a second tag.

---

## Install

Claude Code required. No code, no dependencies, nothing to build — the skill is a single `SKILL.md`.

```bash
git clone https://github.com/happysasha18/product-prover.git
mkdir -p ~/.claude/skills/product-prover
cp product-prover/SKILL.md ~/.claude/skills/product-prover/
```

It also ships inside the [live-spec](https://github.com/happysasha18/live-spec) plugin, if you want the whole pipeline:

```
/plugin marketplace add happysasha18/live-spec
/plugin install live-spec@live-spec
```

Then just ask, in any project:

> *"review this spec"* · *"poke holes in this design"* · *"is this PRD ready — what did I miss?"* · *"Product Prover this"*

---

## What it does

One continuous pass, no pausing between phases.

- **Triage** — is this an analyzable spec at all, or marketing copy? It says so up front rather than pretending.
- **Opening assessment** — the thirty-second verdict: what the document is trying to do, what works, how close it is to buildable.
- **The model** — entities, states and transitions, actors, composition boundaries. Including what it had to *assume* where you were ambiguous, listed explicitly.
- **Structural issues** — incomplete state space, undefined actors, components mixing roles.
- **Property analysis** — safety (invariants, pre/postconditions, atomicity, rollback), liveness (dead ends, silent failure masking), enforceability, internal consistency. Then two tiers of stress lenses. Mandatory sweeps run on every full pass, each owing one recorded verdict — hit, clean, or N/A with a reason — that lands in a surfaces-by-sweeps table, so a skipped sweep never gets mistaken for one that found nothing. These sweeps check that a cross-cutting law reaches every surface, that both ends of a gated range and every state an async result can land in are covered, that same-kind surfaces share the same policy, that a surface's full lifecycle from entry to return holds up, and that no seam was left with an unwritten answer. Imaginative probes follow, with no verdict owed: ties, concurrency, bounds, dependency failures, dangling references. Most produce nothing on most operations, and inventing a finding to satisfy one is a failure.
- **Your acknowledged gaps, kept separate** — the Open Items and TBDs you already flagged are reported *after* the ones you missed, so the signal isn't diluted by things you already know.
- **Human factors** — observability, cognitive load, debuggability. The system that is formally perfect and operationally unusable is a real system.
- **Closing summary** — the top three fixes, properties phrased so you can paste them straight into the spec, and the genuine open questions only you can answer.

**Three review modes:** a full pass over a whole spec, a cross-link pass for one added surface, or a feature-fit pass on a single feature's delta at intake.

**Persisted findings:** written to a dated file with a folded/rejected column, so the next review starts from the last one's open rows instead of relitigating them.

**Shipped systems:** a reconciliation note flags where spec claims may no longer match the code, so findings are conditioned on what actually shipped.

---

## Glossary mode

The terms are half the point. `/glossary liveness`, `/define atomicity`, or just *"what does composition mean?"* — each gives a plain definition, an example, and the question the concept makes you ask in a review.

---

## What counts as a spec

It doesn't know what a PRD is. It knows entities, states, transitions, invariants, preconditions, atomicity, liveness — so any document that implies a state machine is fair game:

- protocol and API designs — retry semantics, idempotency, error contracts
- workflow and approval flows — anything with a status field
- permission and access models
- migration and rollout plans, which are state machines with a deadline
- failure and recovery runbooks
- firmware and device state machines

Two constraints, and they're hard ones. **It needs a document** — not a codebase, not a diagram in your head. It reads what is written and reports what is missing, and there is nothing to read in an undocumented system. (For an existing system, live-spec's [adoption walk](https://github.com/happysasha18/live-spec/blob/main/docs/adoption.md) writes the spec from the code first.) And **the document has to claim behaviour**: point it at a vision deck and triage says so up front rather than pretending to find state machines in it.

Product specs are where it has been used most, and its output leans on that vocabulary. Nothing in the method is product-specific.

---

## What it isn't

It reads documents, not code. It finds holes in what a document *claims*; your test suite proves what the artifact *does*. It is not a substitute for review, either — it is the part of a review that shouldn't depend on which reviewer was in the room that morning.

The judgment stays with you. It is instructed to recommend rather than ask: a reviewer that hands you back a list of questions has moved the work, not done it.

---

## Related

- **[live-spec](https://github.com/happysasha18/live-spec)** — the pack product-prover is the review station of: wish → spec → prove → tests → code → commit, with the spec as the single authority. The prover runs standalone; you don't have to adopt the pipeline.
- **[spec-author](https://github.com/happysasha18/live-spec/tree/main/skills/spec-author)** — the writing half of the pair. It writes the spec; product-prover reviews it.
- **[track-coach](https://github.com/happysasha18/track-coach)** — same instinct, different domain: facts over plausible fiction, and the decision always stays with the author.

---

## Its younger sibling

The prover asks whether the spec holds together as written. Its younger sibling, the design review — the `design-reviewer` skill — reads the same spec right after and asks a different question: whether the design itself is right. Do the things a person acts on the same way actually behave the same way, and what groupings did the text never declare? The prover argues with the sentences on the page; the design review looks into the space between them, where two elements that share a role were never put side by side.

It ships in the same [live-spec](https://github.com/happysasha18/live-spec) pack, so adopting the pipeline brings both passes — the prover first, the design review right behind it.

---

## License

[MIT](LICENSE) © Alexander Abramovich.

*Read-only mirror of one skill from the [live-spec pack](https://github.com/happysasha18/live-spec) — don't open PRs here; changes land in the pack and sync via `scripts/sync-mirrors.sh`.*

---

## Release history

One line per release, generated from the pack's own history at every sync; the full story per release lives in the pack's [JOURNAL.md](https://github.com/happysasha18/live-spec/blob/main/JOURNAL.md).

- 2.4.0 · 2026-07-17 — every budget earns a watcher, the scoped run earns its net, the viewport becomes one banded quantity
- 2.3.0 · 2026-07-16 — the push gate learns proportion, the lens learns depth, the harness learns distrust
- 2.2.0 · 2026-07-16 — mirrors tell their story
- 2.1.1 · 2026-07-16 — the day-after sweep
- 2.1.0 · 2026-07-16 — the enforcement release
- 2.0.0 · 2026-07-16 — the readability + compaction release
- 1.10.1 · 2026-07-15 — the launch sweep clears stale temp litter by age, safely
- 1.10.0 · 2026-07-15 — a cleanup touches only what it owns, never a shared resource in use
- 1.9.0 · 2026-07-15 — the pack grows a third arrow
- 1.8.0 · 2026-07-15 — forward-binding law gets one home, test-infrastructure family becomes a class, harness net hardens
- 1.7.0 · 2026-07-15 — the pack ships the canonical browser test harness
- 1.6.1 · 2026-07-15 — deferral rule gains its mechanical net + delivery arm; build-pipeline thinned
- 1.6.0 · 2026-07-15 — a flaky owned test is a defect fixed at its root
- 1.5.0 · 2026-07-15 — the prover and design review as one bounded loop, design review shipped alongside the prover
- 1.0.9 · 2026-07-10 — the attribution line carries the pack version
- 1.0.8 · 2026-07-10 — the four host checks live
- 1.0.7 · 2026-07-10 — a norm-pointered clause owes a norm-conformance matrix row
- 1.0.6 · 2026-07-10 — the attribution line softens to an OFFER on his same-day correction
- 1.0.5 · 2026-07-10 — everything built with the method says so
- 1.0.4 · 2026-07-10 — the leave-command reaches a shutdown-safe stop
- 0.9.0 · 2026-07-08 — milestone audit
- 0.8.0 · 2026-07-05 — milestone mechanics
- 0.5.0 · 2026-07-05 — preventive audit run + folded

---

made with [live-spec](https://github.com/happysasha18/live-spec) v2.4.0
