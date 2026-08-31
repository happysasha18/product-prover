# Review modes — the two narrower passes and the merge gate

`SKILL.md`'s "Review modes" section names three modes and one gate, and runs the full review's
mechanics in its own numbered phases. This file holds what only a review running the New-surface
review, the Feature-fit review, or the pre-merge gate needs. Open the section below once that mode
or gate is the one in hand.

---

## New-surface review

Seven lenses run in this mode, and all seven live in `reference/stress-lenses.md`:

- declared cross-cutting laws — a mandatory sweep, and it owes a verdict line here. It reads the
  new surface's clause against each declared law, and the new surface's test row beside it;
- edge-condition completeness — a mandatory sweep, and it owes a verdict line here;
- cross-surface policy uniformity — a mandatory sweep, and it owes a verdict line here;
- unwritten seams — a mandatory sweep, and it owes a verdict line here;
- paired-transition symmetry — the lifecycle sweep's sub-question on paired state changes. It owes a
  verdict line here, while the rest of the lifecycle sweep stands down;
- interactive overlap across layers — whether two things can take the same input at once, which
  reads as a modal over a screen, two routes matching one request, or two consumers on one queue;
- delivery separability along a declared axis.

The last two are imaginative probes and owe no verdict.

The record for this mode carries a verdict line for each of the five sweep entries above. Each
line reads hit, clean, or N/A with its reason, the same three verdict words a full review writes.
The five entries here are this mode's own set. A full review's table carries a lifecycle column
where this mode carries paired-transition symmetry alone. The record also carries the class line,
written beneath the verdict table.

This mode skips the property analysis of Phase 3, its steps 3a through 3d. Those steps read the
whole document for safety, liveness, enforceability and internal consistency. Every mandatory
sweep of Phase 3e runs, scoped to the new surface and its seams, with one exception. The lifecycle
sweep sends its paired-transition symmetry sub-question alone, and its other angles stand down
here. A new surface arrives with no clause and no test row yet, so the declared-laws sweep is the
one it most needs.

The mode keeps one whole-document step: the **quantifier re-verify**.

Sweep the document for enumerations and universal quantifiers: "every", "only", "all", "exactly",
and explicit member lists. Re-verify each such sentence against the surface set that now includes
the newcomer. A sentence the newcomer falsifies is a finding at the add. Three shapes carry it:

- a member list that now excludes the newcomer;
- an "only" that now ranges wider;
- a terminal edge that is no longer terminal.

Use this mode on every surface add, where a full re-review would cost more than the change
warrants.

## Feature-fit review

The seven journey seams:

- **arrival** — how the path first reaches the feature: a link followed, an endpoint called, a
  command typed, a message consumed;
- **every next-step** — where the path can go from each point inside the feature;
- **return visit** — what a second pass through the feature meets: a person coming back to it, a
  caller retrying, a job re-running over the same input;
- **cross-entry** — reaching the feature by a door other than the main one: a deep link, a direct
  call that skips the wrapper, a manual replay;
- **implied neighbour state** — what the surfaces around it are doing while it runs: the other
  surfaces present at the same time, the other consumers on the same queue, the neighbouring step
  in the pipeline;
- **the quality bar** — the standard of craft the feature is held to, stated in terms its own kind
  can meet: motion and spacing on a screen, response time and error wording on a service, output
  format and exit codes on a command;
- **invited-next** — what the product offers as the next move once the feature is done: a
  suggested action, a returned link to the created resource, a printed next command.

Those seven hold for a feature of any kind, and a kind with lenses of its own walks those beside
them. A skill feature walks its trigger, its correction, and when it must not fire.

Each lens takes one of four verdicts:

- backed by a clause in the document;
- closed trivially, with how it was closed written down;
- marked as a provisional default;
- a question batched for the author.

The walk also asks the **second-sibling question** by construction. Is anything in this addition a
second member of a kind an existing surface already has? The test is the same one-sentence role as
something already in the document. The role can be the same call shape on another endpoint, the
same flag on another command, or the same gesture on another screen. A yes calls for a
design-consistency review scoped to the new elements against the existing inventory. A no is
recorded as a lens verdict like any other.

This mode runs while the feature is being written, ahead of the full review, and it validates the
fit alone. Pre-existing consistency between old clauses is out of scope for this mode. A new clause
contradicting any existing clause is in scope, and it is the mode's first check. On a document
claiming a shipped system, a "backed by a clause" verdict cites a clause whose surface carries a
current pin (Phase 0). An unpinned clause backs a conditional verdict alone, marked the way Phase 0
marks them. This mode runs most often, so it is the one most exposed to the dead prose the Phase 0
pin requirement exists to catch.

A feature-fit review stands in for no other pass. The feature still meets the full review, or the
new-surface review where that is its mode, before it is built.

## The merge gate: judge the delta

**Reviewing a rewrite before it merges: judge the delta.** A restructure or a migration is gated for
merging back into the main line. That merge gate judges the delta. It has three parts:

- load-bearing token identity, old text against new, modulo the per-chunk named deltas, plus a
  punctuation-multiset check that catches a restructure which preserved every word and changed the
  sentence boundaries.

  A load-bearing token is one word of the document's content, with markup and whitespace left out. A
  chunk is one stretch of the old document the restructure moved as a unit. A named delta is a change
  the restructure's own record declared for that chunk in advance.

  Produce the comparison this way. Build the word-token multiset of the old text and of the new. Build
  the punctuation multiset of each, since word-token identity alone passes a reflow that moved
  punctuation. Set the named deltas aside, and compare each pair. Two runs of this gate must agree, so
  write down the command or the script the project used and keep it with the gate's record. This skill
  ships no such script. Where the project has none either, say so in the record and read the gate's
  token part as not runnable;
- the full test suite green on the merged tree;
- a full review pass on both sides, whose blocking set is scoped to the delta.

Four things block:

- an unmatched token;
- a red suite;
- a finding present on the new side and absent on the old side;
- a meaning change nobody named.

The pass reads the old tree and the merged tree. A finding present on both is pre-existing, and a
finding new to the merged side is delta-scoped. Pre-existing findings become tracked follow-ups in the
same change and never block, so the merge stands free of debts it did not create.

This gate runs where both sides are in reach. A document handed over on its own carries no old side.
The gate then stands down by name, and the pass reads the document as it stands.

The token-identity part applies to a restructure meant to preserve content. A deliberate redesign
changes content by intent. Its merge stands on the green suite and the delta-scoped review pass,
with no token-identity demand over text the redesign meant to change.
