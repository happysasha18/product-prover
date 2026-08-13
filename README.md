**product-prover** — one skill from the [live-spec pack](https://github.com/happysasha18/live-spec), installable on its own. Read-only mirror: do not open PRs here; changes land in the pack and are synced by scripts/sync-mirrors.sh.

# product-prover

**A senior-architect review of your product spec, written as a [Claude Code](https://claude.com/claude-code) skill. It puts [formal-verification](https://en.wikipedia.org/wiki/Formal_verification) questions — states, transitions, invariants, atomicity, liveness — to a document written in prose. The questions are the borrowed part. The pass itself is a careful reading by a model. No solver runs, no script ships, and nothing gates your build.**

Point it at a PRD, feature spec, HLD, architecture document, or design proposal. Four things come
back: a short opening assessment, the structural model it extracted, the gaps that matter, and what to
fix before you build. It is for the person who owns the document. That person is the product manager,
the tech lead, or the founder writing the spec an agent will build from.

---

## Why

A reviewer catches the errors the document gives them words for. A missing rollback, a state with no
exit, an operation that isn't atomic: these have no words on the page to argue with. So nobody argues,
and the spec passes.

That used to be survivable. A human had to read the document before building against it. A person
building against a hole produces friction: a question in grooming, a spike, an argument. An agent
generating from the same document produces no friction at all. It fills the hole with a plausible
default and keeps going. The tests are then derived from the same document, so they say nothing about
the missing property either.

Green suite. Shipped gap. The review has to happen on the document, before anything is generated
from it.

---

## What a finding looks like

Findings arrive in operational terms, each one traced to a quote in your document. This one comes from
a run on 2026-08-05 against `examples/sample-spec.md`, the 95-line fictional parcel-locker spec that
ships in this folder:

> **The 72-hour pickup window is enforced anywhere between hour 72 and hour 96**
>
> *Section "6. Pickup":* "The pickup window is 72 hours from deposit."
>
> **Consequence:** the expiry sweep runs once a day, at 03:00 (Section 7). A parcel stops being collectable when the sweep next runs, and that can land anywhere in the 24 hours after the 72-hour mark. A parcel deposited at 02:00 is refused at hour 73. One deposited at 04:00 is still collectable at hour 94, and the day-4 sweep expires it at hour 95. A recipient told "72 hours" has no way to tell which of the two they are in. A support agent cannot state a deadline that holds either.
>
> **Fix:** pick one and write it into the spec. (a) Expiry is evaluated when the code is entered, and the sweep only moves already-expired parcels for reporting. (b) The sweep runs hourly. (c) The stated window becomes "72 hours, enforced at the next daily sweep". Option (a) makes the promised number true at the keypad, where the recipient meets it, and the sweep keeps its cheap nightly cadence.
>
> `defect · internal-conflict (consistency)`

The formal vocabulary appears only in that last tag. Everything above it is written in the terms your
team already uses.

A model reads the document afresh each time, so two runs over one unchanged file return overlapping
lists of unequal length. That gap measures the run, and the document is the thing held constant.

Two runs over this sample on 2026-08-06 returned 32 and 30 findings, and 24 of them were reached by
both. Their Jaccard overlap is 63%, and their readiness verdicts differ. The full records are in
[`examples/sample-review-run-1.md`](examples/sample-review-run-1.md) and
[`examples/sample-review-run-2.md`](examples/sample-review-run-2.md). They are evidence from edition
1.0.0. Edition 1.1.0 uses the shorter conversation contract below.

Edition 1.1.0 adds a [compact sample response](examples/sample-response.md) and a versioned
[acceptance rubric](evals/sample-spec-rubric.json). The rubric pins seven critical finding classes,
two negative controls, the readiness verdict, and the 1,500-word conversation budget. Raw finding
count is no longer the quality measure.

Read a single count as one careful reader's pass. The findings both runs reached are the ones to act
on first.

Every finding is one of two kinds, and the tag says which. A **defect** is a violated invariant, a
false claim, or a missing required answer; it blocks the build. A **recommendation** is a consistency
or quality gain with nothing broken; it queues for a judgment call, and you decide. Which of the two a
finding is follows from production impact. The same atomicity gap is a recommendation for a manual
quarterly job. It is a defect for an automated path that runs a thousand times a day. The reasoning
stands in the finding's own consequence paragraph, and the tag carries the call alone.

**The rule it won't break:** never produce a finding the reader can't trace back to the document.
Every consequence names who is affected, what triggers it, what breaks, and what they see — "this
could be a problem" fails that bar. Every fix names a specific artifact or decision. Eleven vague
verbs are banned, including `define`, `ensure`, and `consider`. All eleven are listed in `SKILL.md`
under "How to write findings". Where the document is too vague to support a concrete consequence, the
review says so and invents nothing. A reviewer that produces plausible fiction is worse than no
reviewer.

---

## Install

[Claude Code](https://claude.com/claude-code) is required, with the Anthropic account it runs on.
Installing is a copy of two items into your skills directory.

This folder is the source of the standalone package published at
[github.com/happysasha18/product-prover](https://github.com/happysasha18/product-prover). That
repository is a read-only copy: the same `SKILL.md`, `reference/`, and `examples/` you see here.
Install from either one.

```bash
git clone https://github.com/happysasha18/product-prover.git
cd product-prover
mkdir -p ~/.claude/skills/product-prover
cp -R SKILL.md reference ~/.claude/skills/product-prover/
ls ~/.claude/skills/product-prover
# SKILL.md   reference
```

Without git, download
[the zip](https://github.com/happysasha18/product-prover/archive/refs/heads/main.zip), unpack it, and
run the last three commands from the unpacked folder.

Both items have to land: the review opens `reference/stress-lenses.md` partway through the pass, from
inside its own installed directory. Claude Code picks up skills placed in `~/.claude/skills/`
automatically; open a new session if one was already running. Then ask, in any project:

> *"review this spec"* · *"poke holes in this design"* · *"is this PRD ready — what did I miss?"* · *"Product Prover this"*

Name the file in the same message — "review docs/checkout-v2.md" — or paste the document into the
chat. To ask for a narrower pass, name it: *"feature-fit review of the export feature I'm adding"*,
*"new-surface review — I added the /exports endpoint"*. For one term on its own, ask *"glossary:
liveness"*. The package registers no slash command, so write every request as ordinary text.

**The review writes its evidence file into the project it runs in:** `docs/review/YYYY-MM-DD.md`, or
a path you name. It carries every finding, the coverage tables, and a column for whether the fix was
applied or rejected. The conversation stays under 1,500 words by default: verdict, compact model,
three expanded findings, an index of the rest, and readiness. The next review starts from the last
record's open rows.

The reviewed document stays read-only unless you explicitly ask to apply fixes. A review-only pass
leaves paste-ready clauses and `[default]` sentences as proposals. Applying fixes changes the document.

To try it on the sample first: `examples/sample-spec.md` is the parcel-locker spec quoted above,
written with gaps in it. The install leaves it in the folder you downloaded. Open a session there
and ask *"review examples/sample-spec.md"*, then compare what it reports against that finding.

---

## What comes back

One continuous pass runs, with no pausing. It carries triage, a short opening assessment, and the
structural model with an explicit list of what it assumed where you were ambiguous. Then come
structural issues, property analysis, the gaps you flagged yourself reported last, human factors,
and a closing summary.

On a full pass, the property analysis also runs the five mandatory sweeps of
`reference/stress-lenses.md`. Each records a verdict of hit, clean, or not applicable, with its
reason, so a skipped sweep stays distinct from one that passed. Twelve imaginative probes follow in
that file. They owe no verdict; most produce nothing, and inventing a finding to satisfy one is a
failure. The class lens stands beside them, and it owes a line of its own. A defect found at one
spot is swept across the document for its look-alikes, and each pass records whether that sweep ran.

The summary ends on a count of the provisional defaults. A provisional default is a sentence that
states a behaviour and marks it `[default]`, standing until the person who owns that decision confirms
it. The review proposes that marked sentence. It writes it into your document only when you ask it to
apply fixes. The count lists the oldest five, so they stay visible.

**Three modes** exist. You pick one. It is a full pass over a whole spec, a new-surface pass for one
added surface, or a feature-fit pass on one feature being added. The full pass runs when nobody names
a mode.

Where the document describes running code, the review asks each surface for the `file:line` that
carries it. It opens what it is given, with your permission at each read. With no citations it still
runs, and every finding on an already-built part is marked conditional on the document still matching
the code.

---

## Does this fit your document?

It works from entities, states, transitions, invariants, preconditions, atomicity, and liveness. A
document's genre decides nothing. Protocol and API designs, workflow and approval flows, permission
models, migration plans, failure runbooks, firmware state machines, and architecture documents all
qualify. Two constraints are hard. It needs a written document, since a codebase and a diagram in your
head leave it nothing to read. And the document has to claim behaviour: point it at a vision deck and
triage says so up front.

The method assumes no product kind. Every sweep and every lens states its reading in terms. Those
terms hold for a backend service, a protocol, a library, a data pipeline, a command-line tool, or a
screen. Where a reading needs a concrete instance to be understood, it gives two or three from
different kinds. A guarantee's condition band reads as a viewport range on one document and as a
payload size on the next. The state carried across a transition is focus and scroll position in one
document, and an open lease or a half-filled buffer in another. Product specs are where it has been
used most, and that shows in the vocabulary of its output alone.

It finds holes in what a document *claims*, and your test suite proves what the artifact *does*.
Applying a fix, rejecting it, and settling a judgment call stay with you. Market fit, pricing, and
whether the feature is worth building are outside it.

---

## Known issues

- **The two narrow modes were built for a pipeline that selected them.** In the fuller method, another
  step chose the new-surface and feature-fit passes. Here you name the mode yourself, and that
  phrasing has been exercised less than the full pass.
- **A mechanical floor stays your suite's job.** Where the method names one — a coverage test, a
  completeness check across sibling surfaces — the review names its absence in the record.
- **The install was tested by hand, on macOS,** on 2026-08-05, followed by one full review from the
  installed copy against the sample spec. A Windows shell needs its own equivalents of `mkdir` and
  `cp`, and that path is untested here.
- **The trigger phrasing carries no measurement.** The description that tells Claude Code when to load
  the skill asks it to fire on a request for feedback even where the word "review" goes unsaid. How
  often that happens is unmeasured for this edition, so name the skill when you want it for certain.

Two more passes belong beside this one, and are left to their own reviewer. One is whether a stranger
can read the prose. The other is whether the design itself is right. Both ship in
[live-spec](https://github.com/happysasha18/live-spec), the fuller method this skill was lifted from.
It wires this review to a spec author, a test author, and a set of mechanical gates.

Problems go to
[github.com/happysasha18/product-prover/issues](https://github.com/happysasha18/product-prover/issues),
and a gap it missed on your own document is the most valuable report to send.

---

[MIT](LICENSE) © Alexander Abramovich. The skill is prose, so it pulls in no third-party code and
carries no dependency of its own. The sample spec is written for this repository and describes no real
company. This is edition `1.2.0-standalone`: it carries its own version and follows no live-spec
release, so the two move on separate clocks. The live-spec source history appended by the mirror
records provenance. This edition's version stands above.

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
