**product-prover** — the canonical Product Prover, in its own repository with its own version line. The [live-spec pack](https://github.com/happysasha18/live-spec) installs it as an external skill, and everything here runs without the pack. PRs and issues land here.

# product-prover

**Product Prover is a senior-architect review of your product specs and designs, written as a [Claude Code](https://claude.com/claude-code) skill.**

**The internal method puts [formal-verification](https://en.wikipedia.org/wiki/Formal_verification) thinking — states, transitions, invariants, atomicity, liveness — to a document written in prose, and you get the findings back in plain language. No solver runs, no script ships, and nothing gates your build. A limited Code mode extends the same reading to a code-only scope — a directory, a family of sibling scripts, a diff — for repeating defects and incomplete closed sets, scoped short of a general code review.**

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
a run on 2026-08-05 against `examples/sample-spec.md`. That file is the 95-line fictional
parcel-locker spec shipping in this folder:

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
both. Their Jaccard overlap — shared findings over all distinct findings — is 63%, and their readiness verdicts differ. The full records are in
[`examples/sample-review-run-1.md`](examples/sample-review-run-1.md) and
[`examples/sample-review-run-2.md`](examples/sample-review-run-2.md). Read them as evidence of overlap
and judgment, not of today's output length — they predate the shorter conversation contract described
below.

A [compact sample response](examples/sample-response.md) and a versioned
[acceptance rubric](evals/sample-spec-rubric.json) show the expected shape of a review. The rubric pins seven critical finding classes,
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

This repository is the canonical source: `SKILL.md`, `reference/`, and `examples/` live and
version here. The [live-spec](https://github.com/happysasha18/live-spec) pack installs these same
files as an external skill through its own installer. A pack install and a direct install land
identical content.

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

Both items have to land: the review opens `reference/stress-lenses.md` partway through the pass, and
`reference/code-lenses.md` in code mode, from inside its own installed directory. Claude Code picks up skills placed in `~/.claude/skills/`
automatically; open a new session if one was already running. Then ask, in any project:

> *"review this spec"* · *"poke holes in this design"* · *"is this PRD ready — what did I miss?"* · *"Product Prover this"* · *"review scripts/ for a code defect"*

Name the file in the same message — "review docs/checkout-v2.md" — or paste the document into the
chat. To ask for a narrower pass, name it: *"feature-fit review of the export feature I'm adding"*,
*"new-surface review — I added the /exports endpoint"*. For one term on its own, ask *"glossary:
liveness"*. The skill registers no slash command, so write every request as ordinary text.

**The review writes its record into the project it runs in:** `docs/review/YYYY-MM-DD.md`, or
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
`reference/stress-lenses.md`. A sweep walks one check over every member of a class in the document.
Each records a verdict of hit, clean, or not applicable, with its reason, so a skipped sweep stays
distinct from one that passed. Twelve imaginative probes follow in that file. A probe is a what-if
question put to the document. Probes owe no verdict; most produce nothing, and inventing a finding
to satisfy one is a failure. The class lens stands beside them, and it owes a line of its own. Its move: a defect found at one
spot is swept across the document for its look-alikes. Each pass records whether that sweep ran.

The summary ends on a count of the provisional defaults. A provisional default is a sentence that
states a behaviour and marks it `[default]`, standing until the person who owns that decision confirms
it. The review proposes that marked sentence. It writes it into your document only when you ask it to
apply fixes. The count lists the oldest five, so they stay visible.

**Three modes** exist. You pick one. It is a full pass over a whole spec, a new-surface pass for one
added surface, or a feature-fit pass on one feature being added. A surface is a place someone or
something meets the product: an endpoint, a screen, a command, a report. The full pass runs when
nobody names a mode. A pipeline driving the skill may name a mode by its machine name: `FULL`,
`CROSS-LINK`, `FEATURE-FIT`. Both name sets open the same doors.

**Code mode** is a fourth door, for when there is no document at all: a source directory, a family of
sibling scripts, or a diff. Ask "review this code" or "find a defect in scripts/" and triage routes
there instead of refusing the input as a wrong artifact. It carries over three things from the
document pass — a defect found at one spot swept for its look-alikes, the mechanical techniques that
sweep does the work with (grep, a sibling-family walk, a sibling diff, a caller walk), and closed-set
completeness (every enum arm, every implementer, every sibling file handled the same way). It leaves
out what needs a document to check against: declared cross-cutting laws, lifecycle sweeps, provisional
defaults, and three-source disagreement. It does not replace a full code review, and it cannot check
conformance to a spec that does not exist. [`reference/code-lenses.md`](reference/code-lenses.md)
carries the full procedure.

Where the document describes running code, the review asks each surface for the `file:line` that
carries it. It opens what it is given, with your permission at each read. With no citations it still
runs, and every finding on an already-built part is marked conditional on the document still matching
the code.

---

## Does this fit your document?

It works from entities, states, transitions, invariants, preconditions, atomicity, and liveness. A
document's genre decides nothing. Protocol and API designs, workflow and approval flows, permission
models, migration plans, failure runbooks, firmware state machines, and architecture documents all
qualify. Two constraints are hard. It needs a written document, or, where none exists, code mode's own
narrower ground: a source directory, a family of sibling scripts, or a diff, with no diagram-in-your-
head substitute for either. And the document has to claim behaviour: point it at a vision deck and
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

- **The two narrow document modes were built for a pipeline that selected them.** In the fuller
  method, another step chose the new-surface and feature-fit passes. Here you name the mode yourself,
  and that phrasing has been exercised less than the full pass. Code mode is a separate door, for
  input with no document at all, and this known issue does not cover it.
- **A mechanical floor stays your suite's job.** Where the method names one — a coverage test, a
  completeness check across sibling surfaces — the review names its absence in the record.
- **The install was tested by hand, on macOS,** on 2026-08-05, followed by one full review from the
  installed copy against the sample spec. A Windows shell needs its own equivalents of `mkdir` and
  `cp`, and that path is untested here.
- **The trigger phrasing carries no measurement.** The description that tells Claude Code when to load
  the skill asks it to fire on a request for feedback even where the word "review" goes unsaid. How
  often that happens is unmeasured for this release, so name the skill when you want it for certain.

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
company. This is release `1.4.2`, and this repository's version line is the only one the skill follows.

---

## Release history

See [CHANGELOG.md](CHANGELOG.md).

---

grown in [live-spec](https://github.com/happysasha18/live-spec) · standing on its own since 1.0.0
