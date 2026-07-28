**product-prover** — one skill from the [live-spec pack](https://github.com/happysasha18/live-spec), installable on its own. Read-only mirror: do not open PRs here; changes land in the pack and are synced by scripts/sync-mirrors.sh.

# product-prover

**A senior-architect review of your product spec, through the lens of [formal verification](https://en.wikipedia.org/wiki/Formal_verification). A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a PRD, feature spec, HLD, or design proposal. It reads the document the way a principal architect would. You get four things back: a short verdict, the structural model it extracted, the gaps that matter, and what to fix before you build.

---

## Why

A spec passes review because a reviewer catches errors in the language the document is written in. A missing rollback, a state with no exit, an operation that isn't atomic: these have no words on the page to argue with. So nobody argues.

That used to be survivable. A human had to read the document before building against it. A person building against a hole produces friction: a question in grooming, a spike, an argument. An agent generating from the same document produces no friction at all. It fills the hole with a plausible default and keeps going. The tests are then derived from the same document, so they say nothing about the missing property either.

Green suite. Shipped gap. The review has to happen on the document, before anything is generated from it.

---

## What a finding looks like

Findings arrive in operational terms, each one traced to a quote in your document. Illustrative:

> **A failed update can be silently overwritten by the next one**
>
> *Spec §4.2:* "If the update fails, the tenant enters `Failed to Update`." The document defines no transition out of that state. §4.3 allows a new update from any state.
>
> **Consequence:** a tenant whose update failed at 14:02 receives a second update at 14:05 that succeeds. The tenant now reads `Updated`. The billing service that consumed the first update never learns it was lost, and no operator sees an error. The failure is gone from the record.
>
> **Fix:** state the exit from `Failed to Update`. Three answers fit: a retry, a revert to the last consistent state, or a hard stop that alerts an operator. Then state whether a new update is accepted before that exit is taken.
>
> `defect · stuck-state (liveness)`

The formal vocabulary appears only in that last tag. The framework stays private; you get the finding.

Every finding is one of two kinds, and the tag says which. A **defect** is a violated invariant, a false claim, or a missing required answer. It blocks the build, and it is folded into the spec before you ship. A **recommendation** is a consistency or quality gain with nothing broken. It queues for a taste call, and you decide.

---

## The rule it won't break

> Never produce a finding the reader can't trace back to the document.

Every finding quotes its source and pins the location. Every consequence is concrete: who is affected, what triggers it, what breaks, and what they see. "This could be a problem" fails that bar. Every fix names a specific artifact or decision, and the vague verbs are banned: `define`, `ensure`, `handle`, `consider`. When the document is too vague to support a concrete consequence, it says so plainly and invents nothing.

An adversarial reviewer that produces plausible fiction is worse than no reviewer.

The verdict tracks production impact, and formal purity leaves it alone. The same atomicity gap is a recommendation for a manual quarterly job. It is a defect for an automated path that runs a thousand times a day. The reasoning lives in the finding, and a second tag never carries it.

---

## Install

Claude Code required. The skill is a single `SKILL.md` file, and installing it is a copy.

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

Point it at any PRD, design doc, or ARCHITECTURE.md. Claude Code picks up skills placed in `~/.claude/skills/` automatically. Open a new session if one was already running when you installed it.

---

## What it does

One continuous pass, no pausing between phases.

- **Triage** — is this an analyzable spec at all, or marketing copy? It says so up front, and it reports plainly when the document holds no spec.
- **Opening assessment** — the thirty-second verdict: what the document is trying to do, what works, how close it is to buildable.
- **The model** — entities, states and transitions, actors, and composition boundaries. It lists explicitly what it had to *assume* where you were ambiguous.
- **Structural issues** — incomplete state space, undefined actors, components mixing roles.
- **Property analysis** — safety, meaning invariants, preconditions and postconditions, atomicity, and rollback; liveness, meaning dead ends and silent failure masking; enforceability; and internal consistency. Then, on a full pass, it runs a fixed set of completeness checks. Each one records a verdict: found something, clean, or not applicable. A skipped check therefore stays distinct from one that passed. The checks cover:
  - whether a rule meant to apply everywhere reaches every screen
  - whether both ends of every range are handled
  - whether every loading/loaded/failed outcome has a defined UI
  - whether similar screens follow the same policy
  - whether a screen's whole lifecycle holds from entry back to return
  - whether any seam is left with an unwritten answer

  Imaginative probes follow, with no verdict owed: ties, concurrency, bounds, dependency failures, and dangling references. Most produce nothing on most operations, and inventing a finding to satisfy one is a failure.
- **Your acknowledged gaps, kept separate** — the Open Items and TBDs you already flagged are reported *after* the ones you missed. The things you already know then leave the signal intact.
- **Human factors** — observability, cognitive load, debuggability. The system that is formally perfect and operationally unusable is a real system.
- **Closing summary** — five short blocks. The top three fixes. Properties phrased so you can paste them straight into the spec. The genuine open questions only you can answer. The recommendations queued for a taste call, held apart from the defects that fold first. And, on a full pass, a running count of the placeholder decisions still sitting in the document, oldest first, so they stay visible.

**Three review modes:** a full pass over a whole spec, a cross-link pass for one added surface, and a feature-fit pass on one feature's delta. Used on its own, the skill runs the full pass. The cross-link and feature-fit passes are selected automatically when this skill runs inside the live-spec pipeline.

**Persisted findings:** written to a dated file carrying each finding's kind, a folded-or-rejected column, and the verdict table for the mandatory sweeps. The next review then starts from the last one's open rows, and it leaves the settled ones settled.

**Shipped systems:** a reconciliation note flags where spec claims may no longer match the code, so findings are conditioned on what actually shipped.

---

## Glossary mode

The terms are half the point. Ask `/glossary liveness`, `/define atomicity`, or *"what does composition mean?"*. Each answer gives a plain definition, an example, and the question the concept makes you ask in a review.

---

## What counts as a spec

It works from entities, states, transitions, invariants, preconditions, atomicity, and liveness, rather than from a document's genre. Any document that implies a state machine is fair game:

- protocol and API designs — retry semantics, idempotency, error contracts
- workflow and approval flows — anything with a status field
- permission and access models
- migration and rollout plans, which are state machines with a deadline
- failure and recovery runbooks
- firmware and device state machines
- architecture documents (an `ARCHITECTURE.md` or HLD) — read through their own lens:
  - which node owns each fact
  - nodes that only speculate
  - the seams between them
  - budgets and the observer that watches each
  - the runtime and placement views
  - a re-ask when a node has grown past its stated job

Two constraints, and they are hard ones.

**It needs a document.** A codebase, and a diagram in your head, leave it nothing to read. It reads what is written and reports what is missing, and an undocumented system offers neither. For an existing system, live-spec's [adoption walk](https://github.com/happysasha18/live-spec/blob/main/docs/adoption.md) writes the spec from the code first.

**The document has to claim behaviour.** Point it at a vision deck and triage says so up front. It reports the absence of state machines and invents none.

Product specs are where it has been used most, and its output leans on that vocabulary. Nothing in the method is product-specific.

---

## What it leaves to others

It reads documents, and code stays outside its reach. It finds holes in what a document *claims*, and your test suite proves what the artifact *does*. It is one part of a review: the part that stays the same whichever reviewer was in the room that morning.

The judgment stays with you. It is instructed to recommend: a reviewer that hands you back a list of questions has shifted the work onto you and finished nothing.

---

## Related

- **[live-spec](https://github.com/happysasha18/live-spec)** — the pack product-prover is the review station of. Its pipeline runs wish → spec → prove → tests → code → commit, and the spec is the single authority. The prover also runs on its own, with the pipeline left aside.
- **[spec-author](https://github.com/happysasha18/live-spec/tree/main/skills/spec-author)** — the writing half of the pair. It writes the spec; product-prover reviews it.
- **[track-coach](https://github.com/happysasha18/track-coach)** — the same instinct in another domain: facts over plausible fiction, and the decision always stays with the author.

---

## Its younger sibling

The prover asks whether the spec holds together as written. Its younger sibling is the design review, the `design-reviewer` skill. It reads the same spec right after, and it asks whether the design itself is right. Do the things a person acts on the same way actually behave the same way, and what groupings did the text never declare? The prover argues with the sentences on the page. The design review checks whether elements that share a role behave alike, even where the text never put them side by side.

It ships in the same [live-spec](https://github.com/happysasha18/live-spec) pack, so adopting the pipeline brings both passes: the prover first, and the design review right behind it.

---

## License

[MIT](LICENSE) © Alexander Abramovich.

*Read-only mirror of one skill from the [live-spec pack](https://github.com/happysasha18/live-spec). Changes land in the pack and reach this mirror through `scripts/sync-mirrors.sh`, so open pull requests against the pack.*

---

## Release history

One line per release, generated from the pack's own history at every sync; the full story per release lives in the pack's [JOURNAL.md](https://github.com/happysasha18/live-spec/blob/main/JOURNAL.md).

- 3.6.0 · 2026-07-21 — INV-249 — inbox deposit protocol for concurrent windows
- 3.5.0 · 2026-07-21 — INV-248 — delivery-separability prover lens
- 3.4.0 · 2026-07-21 — INV-247 — re-derive a deferred item's state from code before resuming
- 3.3.0 · 2026-07-21 — finalize four-movement integration
- 3.1.0 · 2026-07-20 — the conduct-audit movement closes
- 3.0.0 · 2026-07-20 — the back-describe migration
- 2.9.0 · 2026-07-20 — the comms/naming machinery
- 2.8.3 · 2026-07-20 — the hedge gate reds the common offering-hedge frames
- 2.8.2 · 2026-07-19 — the register judge catches grading-worth-without-fact and unglossed-jargon
- 2.8.1 · 2026-07-18 — the register judge holds base rule 2
- 2.8.0 · 2026-07-18 — the clean-context review law
- 2.7.1 · 2026-07-18 — patch version stamp across skills, plugin.json, and the spec title
- 2.7.0 · 2026-07-18 — the movement's release
- 2.6.0 · 2026-07-17 — agents learn to talk, and a law with no machine is a wish
- 2.5.0 · 2026-07-17 — docs, gate records with addenda, version stamps
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

made with [live-spec](https://github.com/happysasha18/live-spec) v4.3.0
