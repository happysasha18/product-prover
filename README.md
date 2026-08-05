**product-prover** — one skill from the [live-spec pack](https://github.com/happysasha18/live-spec), installable on its own. Read-only mirror: do not open PRs here; changes land in the pack and are synced by scripts/sync-mirrors.sh.

# product-prover

**A senior-architect review of your product spec, through the lens of [formal verification](https://en.wikipedia.org/wiki/Formal_verification). A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a PRD, feature spec, HLD, architecture document, or design proposal. It reads the document the way a principal architect would. You get four things back: a short verdict, the structural model it extracted, the gaps that matter, and what to fix before you build.

It is for the person who owns the document — the product manager, the tech lead, the founder writing the spec an agent will build from. Install it with a copy, then ask for a review in plain words.

---

## Why

A spec passes review because a reviewer can only catch the errors the document gives them words for. A missing rollback, a state with no exit, an operation that isn't atomic: these have no words on the page to argue with. So nobody argues.

That used to be survivable. A human had to read the document before building against it. A person building against a hole produces friction: a question in grooming, a spike, an argument. An agent generating from the same document produces no friction at all. It fills the hole with a plausible default and keeps going. The tests are then derived from the same document, so they say nothing about the missing property either.

Green suite. Shipped gap. The review has to happen on the document, before anything is generated from it.

---

## What a finding looks like

Findings arrive in operational terms, each one traced to a quote in your document. This one comes from a run on 2026-08-05, against `examples/sample-spec.md`, the fictional parcel-locker spec that ships in this folder:

> **The 72-hour pickup window is enforced anywhere between hour 72 and hour 96**
>
> *Section "6. Pickup":* "The pickup window is 72 hours from deposit."
>
> **Consequence:** the expiry sweep runs once a day at 03:00 (Section 7), so a parcel stops being collectable when the sweep next runs rather than at the 72-hour mark. A parcel deposited at 02:00 is refused at hour 73. One deposited at 04:00 is still collectable at hour 94, and the day-4 sweep expires it at hour 95. A recipient told "72 hours" has no way to tell which of the two they are in, and a support agent cannot state a deadline that holds.
>
> **Fix:** pick one and write it into the spec. (a) Expiry is evaluated when the code is entered, and the sweep only moves already-expired parcels for reporting. (b) The sweep runs hourly. (c) The stated window becomes "72 hours, enforced at the next daily sweep". Option (a) makes the promised number true at the keypad, where the recipient meets it, and the sweep keeps its cheap nightly cadence.
>
> `defect · internal-conflict (consistency)`

That run returned 22 findings on the 95-line document in `examples/`, plus commentary on the three gaps the document flags itself. A second run over the same document returned 14. Counts move between runs, so treat a count as a rough measure of how much a document has to say. The findings both runs reached are the ones to act on first.

The formal vocabulary appears only in that last tag. The framework stays behind the finding.

Every finding is one of two kinds, and the tag says which. A **defect** is a violated invariant, a false claim, or a missing required answer. It blocks the build, and it gets written into the spec before you ship. A **recommendation** is a consistency or quality gain with nothing broken. It queues for a judgment call, and you decide.

---

## The rule it won't break

> Never produce a finding the reader can't trace back to the document.

Every finding quotes its source and pins the location. Every consequence is concrete: who is affected, what triggers it, what breaks, and what they see. "This could be a problem" fails that bar. Every fix names a specific artifact or decision, and eleven vague verbs are banned, `define`, `ensure`, `handle`, and `consider` among them. When the document is too vague to support a concrete consequence, it says so and invents nothing.

An adversarial reviewer that produces plausible fiction is worse than no reviewer.

The verdict tracks production impact, and formal purity leaves it alone. The same atomicity gap is a recommendation for a manual quarterly job. It is a defect for an automated path that runs a thousand times a day. The reasoning lives in the finding, and a second tag never carries it.

---

## Install

Claude Code is required. Installing is a copy of two items into your skills directory.

First get the files. Clone the repository:

```bash
git clone https://github.com/happysasha18/product-prover.git
cd product-prover
```

Without git, download
[the zip](https://github.com/happysasha18/product-prover/archive/refs/heads/main.zip), unpack it, and
open a shell in the unpacked folder.

Then, from the folder that holds this README:

```bash
mkdir -p ~/.claude/skills/product-prover
cp -R SKILL.md reference ~/.claude/skills/product-prover/
```

Check what landed:

```bash
ls ~/.claude/skills/product-prover
# SKILL.md   reference
```

Both have to be there. The review opens `reference/stress-lenses.md` partway through the pass, and it
resolves that path inside its own installed directory.

Then ask, in any project:

> *"review this spec"* · *"poke holes in this design"* · *"is this PRD ready — what did I miss?"* · *"Product Prover this"*

Point it at any PRD, design doc, or architecture document. Claude Code picks up skills placed in `~/.claude/skills/` automatically. Open a new session if one was already running when you installed it.

To ask for a narrower pass, name it:

> *"feature-fit review of the export feature I'm adding"* · *"new-surface review — I added the settings panel"*

### Try it on the sample

`examples/sample-spec.md` is a short fictional spec for a parcel-locker service, written with gaps in
it. The install copies `SKILL.md` and `reference` alone, so the sample stays in the folder you
downloaded. Open a Claude Code session in that folder and ask:

> *"review examples/sample-spec.md"*

From any other folder, give the sample's full path.

The finding shown earlier came from a run against that document, so you can compare what your session
reports with what is printed above. A second run over the same file reported that window gap too,
inside a shorter list — the overlap between two runs is real, and the length of the list moves.

### What is in this folder

| File | What it is |
|---|---|
| `SKILL.md` | The skill itself. This is what Claude Code loads. |
| `reference/stress-lenses.md` | The stress lenses the review opens partway through a full pass. Installs beside `SKILL.md`. |
| `examples/sample-spec.md` | The fictional spec above, for trying the skill out. |
| `README.md` | This page. |
| `PROVENANCE.md` | How this edition was derived from the fuller method, rule by rule. The author's own record. |
| `LICENSE` | MIT. |

---

## What it does

One continuous pass, no pausing between phases.

- **Triage** — is this an analyzable spec at all, or marketing copy? It says so up front, and it reports plainly when the document holds no spec.
- **Opening assessment** — the thirty-second verdict: what the document is trying to do, what works, how close it is to buildable.
- **The model** — entities, states and transitions, actors, and composition boundaries. It lists explicitly what it had to *assume* where you were ambiguous.
- **Structural issues** — incomplete state space, undefined actors, components mixing roles.
- **Property analysis** — safety, meaning invariants, preconditions and postconditions, atomicity, and rollback; liveness, meaning dead ends and silent failure masking; enforceability; and internal consistency. Then, on a full pass, it runs five mandatory sweeps. Each one records a verdict: found something, clean, or not applicable. A skipped sweep therefore stays distinct from one that passed. The five ask:
  - whether a rule meant to apply everywhere reaches every screen
  - whether every range end and every loading, loaded, and failed outcome has a written answer
  - whether similar screens follow the same policy
  - whether a screen's whole lifecycle holds from entry back to return
  - whether any seam is left with an unwritten answer

  Thirteen imaginative probes follow, with no verdict owed: ties, concurrency, bounds, dependency failures, and dangling references among them. Most produce nothing on most operations, and inventing a finding to satisfy one is a failure.
- **Your acknowledged gaps, kept separate** — the Open Items and TBDs you already flagged are reported *after* the ones you missed. The things you already know then leave the signal intact.
- **Human factors** — observability, cognitive load, debuggability. The system that is formally perfect and operationally unusable is a real system.
- **Closing summary** — five short blocks. The top three fixes. Properties phrased so you can paste them straight into the spec. The genuine open questions only you can answer. The recommendations queued for a judgment call, held apart from the defects that get written in first. And, on a full pass, a running count of the sentences still marked as provisional defaults (`[default]`), oldest first, so they stay visible.

**Three review modes,** and you pick: a full pass over a whole spec, a new-surface pass for one added surface, and a feature-fit pass on one feature being added. The full pass is what runs when nobody names a mode.

**Persisted findings:** written to `docs/review/YYYY-MM-DD.md` in the project under review, or to a path you name. The file carries each finding's kind, a column recording whether it was applied or rejected, and the verdict table for the mandatory sweeps. The next review then starts from the last one's open rows, and it leaves the settled ones settled.

**Shipped systems:** where the document claims to describe running code, the review asks for `file:line` citations first and opens the lines it is given. Findings on the already-built parts are marked conditional on the document still matching the code when no citation comes.

---

## Glossary mode

The terms are half the point. Ask in ordinary words: *"glossary: liveness"*, *"define atomicity"*, or
*"what does composition mean?"*. Each answer gives a plain definition, an example, and the question
the concept makes you ask in a review.

This package registers no slash command. A message that opens with a slash reaches Claude Code's own
command picker, so write the request as plain text.

---

## What counts as a spec

It works from entities, states, transitions, invariants, preconditions, atomicity, and liveness, rather than from a document's genre. Any document that implies a state machine is fair game:

- protocol and API designs — retry semantics, idempotency, error contracts
- workflow and approval flows — anything with a status field
- permission and access models
- migration and rollout plans, which are state machines with a deadline
- failure and recovery runbooks
- firmware and device state machines
- architecture documents — read through their own lens, seven checks:
  - which part of the system owns each fact
  - parts the requirements never asked for
  - the seams between the parts, and which side owns each format
  - each quality budget, and the watcher, meaning the check that fails past the stated number
  - which flows the runtime view walks
  - where every part runs
  - a re-check when a part has grown past its stated job

The ownership check reads against the paired requirements document. Where no such document exists,
the review records that one check as not runnable with the reason and runs the other six.

Two constraints, and they are hard ones.

**It needs a document.** A codebase, and a diagram in your head, leave it nothing to read. It reads what is written and reports what is missing, and an undocumented system offers neither. For an existing system, write the spec from the code first.

**The document has to claim behaviour.** Point it at a vision deck and triage says so up front. It reports the absence of state machines and invents none.

Product specs are where it has been used most, and its output leans on that vocabulary. Nothing in the method is product-specific.

---

## What it leaves to others

It finds holes in what a document *claims*, and your test suite proves what the artifact *does*. It is one part of a review: the part that stays the same whichever reviewer was in the room that morning.

Two more passes belong beside it. This skill names them and leaves them to their own reviewer:

- **whether a stranger can read the prose** — an undefined term, a sentence read twice, a comprehension stop;
- **whether the design itself is right** — whether things a person acts on the same way behave the same way, and which groupings the text never declared.

The judgment stays with you. It is instructed to recommend: a reviewer that hands you back a list of questions has shifted the work onto you and finished nothing.

---

## What it cannot do

- **It cannot audit your code.** The review reads the document you point it at. Where that document
  describes running code, the review opens the `file:line` a claim cites and may run a command to
  read the output. Claude Code asks your permission before each file read and each command. A claim
  it cannot check that way is marked conditional on the document still matching the code.
- **It ships no scripts and no gates.** This package is prose: `SKILL.md` and
  `reference/stress-lenses.md`. Every check is a reading discipline a model follows, and a project
  that wants a mechanical floor builds that floor in its own suite. The pass does write one file, the
  dated record described above.
- **It cannot tell you whether the idea is right.** Market fit, pricing, and whether the feature is
  worth building are outside it. It checks whether the document holds together.
- **It cannot review what nobody wrote down.** A codebase with no spec leaves it nothing to read.
- **It repeats itself only roughly.** Two sessions over the same document return overlapping sets of
  findings of unequal length, because a model reads the document each time. Treat a single run as one
  careful reader's pass.
- **It decides nothing.** Applying a fix, rejecting it, and settling a judgment call stay with the
  author.

---

## Reporting a problem

Open an issue at
[github.com/happysasha18/product-prover/issues](https://github.com/happysasha18/product-prover/issues).

The useful report says what kind of document you pointed it at, which mode you asked for, what the
review said, and what you expected instead. A missed gap you found yourself is the most valuable one
to send, and a short description of the document's shape is enough when the document itself is
private.

---

## Known issues

- **The two narrow modes were built for a pipeline that selected them.** In the full method this skill was lifted from, another step chose the new-surface and feature-fit passes automatically. Here you name the mode yourself, and that phrasing has less mileage on it than the full pass.
- **Parts of the sweeps assume a visual product.** Edge-condition completeness carries a viewport reading. Lifecycle carries focus, selection, scroll, playback and sound readings, and the unwritten-seam sweep names its axes in screen terms. An author of a backend, protocol, or physical-system spec translates those readings or records N/A with the reason. Every N/A verdict carries its reason and stays on the record, so expect N/A rows on a non-visual document.
- **No mechanical check ships with this skill.** Every rule here is a reading discipline a model follows. Where the method names a mechanical floor — a coverage test, a completeness check across sibling surfaces — that floor lives in your project's own suite, and the review names its absence rather than supplying it.
- **The stress lenses are long.** `reference/stress-lenses.md` holds the five mandatory sweeps and thirteen imaginative probes. On a small document most of them return clean, and the verdict table is what makes that readable.
- **The install was tested by hand, on macOS.** The commands above were run on 2026-08-05, followed by one full review from the installed copy against the sample spec. A Windows shell needs its own equivalents of `mkdir` and `cp`, and that path is untested here.
- **The trigger phrasing carries no measurement.** The description that tells Claude Code when to load the skill came over from the fuller method. Asking in the words above works. How often the skill fires on its own when the word "review" goes unsaid is unmeasured for this edition, so name the skill when you want it for certain.

---

## Related

- **[live-spec](https://github.com/happysasha18/live-spec)** — the fuller method this skill was lifted from. Its pipeline runs wish → spec → prove → tests → code → commit, and the spec is the single authority. That version wires this review to a spec author, a design review, a test author, and a set of mechanical gates.
- **[track-coach](https://github.com/happysasha18/track-coach)** — the same instinct in another domain: facts over plausible fiction, and the decision always stays with the author.

---

## License

[MIT](LICENSE) © Alexander Abramovich. The skill is prose, so it pulls in no third-party code and
carries no dependency of its own. The sample spec is written for this repository and describes no real
company.

Made with [live-spec](https://github.com/happysasha18/live-spec), the fuller method this skill was
lifted from. This is edition `1.0.0-standalone`: it carries its own version and follows no live-spec
release, so the two move on separate clocks.

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
