# Provenance — how the internal codes were resolved

The version of this skill that runs inside its original method cites internal rule codes as the
authority behind many of its instructions: `SPEC INV-141`, `M-6`, `base rule 14`, and about fifty
others. Those codes index requirements in a private requirements document. A reader outside that
project cannot look them up.

This edition keeps every instruction the codes carried and states the reason in plain words. The
table below records each code, the rule it stood for, and where that rule now lives.

The original requirements document stays private, so this table is the author's own record of the
rewrite. Using the skill asks nothing of it.

Two files carry the resolved text: `SKILL.md` and `reference/stress-lenses.md`. The column "Where it
landed" names one of them.

| Code | The rule it stood for | Where it landed |
|---|---|---|
| INV-4 | Where a decision can be grounded in evidence, decide it and proceed on the recommended answer; keep the open question visible rather than halting on it. | stress-lenses, paired-transition symmetry: an open motion question is surfaced and holds nothing back. |
| INV-15 | A duty binds forward, and where a document is silent on a broken behaviour the document is fixed first so the review can flag it, with the code fix landing under that. | stress-lenses, scenario entry and exit ("the duty binds forward") and the class lens ("the fix to the document comes before the fix to the code"). |
| INV-16 | A request that asks to have something in the product is a feature and goes through the full process; a request that only asks to see or try something stays a fenced sketch. | stress-lenses, unbacked surfaces and unlabelled sketches. |
| INV-17 | Influence crosses out of a prototype and never into a production surface: no wiring, no linking, no styling a production surface to match one. | stress-lenses, unbacked surfaces ("nothing in the shipped product reaches into it"). |
| INV-18 | Every facet is written as a decided sentence or a sentence marked as a provisional default; a blank one is a defect. | SKILL.md word list ("provisional default"); stress-lenses, unwritten seams and the named-part ask. |
| INV-29 | Before a feature is written up, walk its journey seams against the existing document and close what is derivable. | SKILL.md, the feature-fit review mode. |
| INV-30 | Verification walks the product as a visitor would, and a question only the decision-owner can answer is surfaced to them. | SKILL.md and stress-lenses, wherever a question is surfaced to "the person who owns the decision". |
| INV-31 | A taste default is taken without asking, reported in plain words, marked as a default, and never re-confirmed. | SKILL.md word list; stress-lenses, the named-part ask and unwritten seams. |
| INV-36 | Each project declares its kind, and that kind sets the scale at which the architecture checks are judged. | SKILL.md, Phase 0 architecture lens, the list of kinds. |
| INV-37 | Each item is classified at intake and routed to the home that owns it: a new feature, a changed feature, or a restructure. | stress-lenses, three-source disagreement: each of the three shapes routes to its own home. |
| INV-39 | A landing commit carries one item's delta and runs the full suite on a clean tree. | SKILL.md, reviewing a rewrite before it merges: "the full test suite green on the merged tree". |
| INV-41 | Every measurable quality budget names its watcher, the mechanical check that fails past the number, or a decided sentence naming why a person reads it by eye. | SKILL.md, Phase 0 architecture lens, budget check. |
| INV-43 | An approved look is frozen as a dated copy and cited from the governing clause by a pointer, which never reaches into a live prototype directory. | stress-lenses, approved-look clauses. |
| INV-49 | A dependency edge between parallel work items is drawn only on a true dependency or a same-section collision, never on co-location in a shared document. | stress-lenses, false serialization and over-broad independence. |
| INV-50 | Every conditionally-entered face states its deliberate re-entry path, or states the one-way as a decision by name. | stress-lenses, entry symmetry. |
| INV-72 | Walk every axis a stateful surface passes through, and report any reachable situation the document leaves unanswered. This is the blank-answer class most other composition lenses cite. | stress-lenses, unwritten seams; the phrase "blank-answer class" is defined at first use in edge-condition completeness. |
| INV-74 | Every flow the requirements promise is walkable end to end, and every named failure point carries its fallback. | SKILL.md, Phase 0 architecture lens, runtime view check. |
| INV-75 | The architecture states where every node runs, with its load-bearing technology, in a placement view of its own. | SKILL.md, Phase 0 architecture lens, placement view check. |
| INV-101 | Cross-cutting laws live in one declared home, and every surface carries that law's clause or a dated exemption. | stress-lenses, declared cross-cutting laws. |
| INV-111 | A restructure proves content survived by a word-token check and a punctuation-multiset check, since word-token identity alone passes a reflow that moved punctuation. | SKILL.md, reviewing a rewrite before it merges. |
| INV-113 | A deliberate redesign reshapes the architecture document and re-proves it, rather than pinning fresh line numbers onto a stale shape. | SKILL.md, reviewing a rewrite: the token-identity demand stands down for text the redesign meant to change. |
| INV-114 | A restructure or migration merge is judged on the delta alone: content identity, a green suite, and a review pass whose blocking set is scoped to what changed. | SKILL.md, reviewing a rewrite before it merges, and the defect kind's one exception. |
| INV-121 | Check whether an already-proven artifact settles a design question before raising it as a fork; derive and cite where one does. | stress-lenses, three-source disagreement: the read that tells whether a proven artifact settles a question. |
| INV-122 | A new part of the architecture answers three fitness questions: can it be tested alone, does a real second place need it, and can it and its neighbour be worked on in parallel without queuing on the same files. | SKILL.md, Phase 0 architecture lens, second and seventh checks. |
| INV-124 | A confirmed defect is named as a class, every sibling is swept, a structural cause is fixed in the architecture, and a silent document is completed first. | stress-lenses, the class lens's three questions. |
| INV-125 | A policy governing a kind that recurs across sibling surfaces is stated once at the class level, naming the class and enumerating its members. | stress-lenses, cross-surface policy uniformity. |
| INV-126 | Where one direction of a paired state change is designed, the opposite direction is specified too, symmetric by default unless a written reason parts them. | stress-lenses, paired-transition symmetry. |
| INV-127 | Every person-facing scenario states its entry and its exit, including a trivially-none edge stated as such. | stress-lenses, scenario entry and exit. |
| INV-128 | A change is read against the document, the architecture, and the code at one intake moment, and its footprint is named. | stress-lenses, three-source disagreement. |
| INV-136 | A visual project declares its design principles and runs each at verification; among them, two interactive controls from different layers never share a clickable region. | stress-lenses, interactive overlap across layers. |
| INV-138 | A transition gated on a quantity states its behaviour at both ends of the range; an async slot names pending, arrived, and failed; a layout guarantee names its viewport quantifier. | stress-lenses, edge-condition completeness. |
| INV-140 | Every finding is a blocking defect or a queued recommendation, and the kind is read from the finding's own ground. | SKILL.md, the KIND block; also the acknowledged-gap tag. |
| INV-141 | The design review reads the same document after this pass, builds its own inventory of the elements a person acts on, groups the same-kind ones, and produces recommendations rather than blockers. | SKILL.md, "Work that belongs elsewhere" and the design-review keying list; stress-lenses, wherever a design-consistency review is named. |
| INV-144 | Where the product and the document disagree, the document is the definition of correct; changing the document is a decision its owner ratifies. | stress-lenses, three-source disagreement, closing paragraph. |
| INV-150 | Every declared law names its enforcer, chosen by what kind of evidence decides a violation: a mechanical gate, this review, or a design review's recommendation. A law with no enforcer is a broken invariant. | stress-lenses, declared cross-cutting laws, third demand. |
| INV-156 | Every review pass writes its dated record in one shared shape, so a later reader reads each pass the same way. | SKILL.md, persisting the record. |
| INV-165 | An opening gesture is checked for a mirroring closing gesture by construction, and its findings recommend rather than block. | stress-lenses, paired-transition symmetry, the kind read. |
| INV-167 | A surface that can be left and re-entered states where it opens and whether entry resets or resumes prior state. | stress-lenses, entry state. |
| INV-168 | Every stated transition names each parameter a person perceives across it: focus, selection, scroll, playback, sound, timers, freshness. | stress-lenses, transition payload. |
| INV-169 | A feature that adds a second member of an existing kind draws a scoped design review at intake; a no is recorded as a verdict. | SKILL.md, the second-sibling question in the feature-fit mode. |
| INV-170 | Adding a surface re-verifies every universally quantified sentence against the now-larger set. | SKILL.md, the quantifier re-verify in the new-surface mode. |
| INV-171 | Each mandatory sweep owes one verdict line in the record — hit, clean, or not applicable with its reason — and a missing line reads as skipped. | SKILL.md, Phase 3e; stress-lenses, opening section. |
| INV-214 | Parallel lanes open whenever the graph allows, and a session that goes serial names the standing reason. | stress-lenses, false serialization: judging a false edge stays a senior read. |
| INV-215 | A paragraph carrying three or more parallel facts is rendered as a list; laws and their reasoning stay prose. | SKILL.md, the cognitive-load row of the category table. |
| INV-233 | Nodes per file are counted from the architecture's own pin column, and that count is held as a ceiling that only tightens. Raw file size is the wrong signal. | SKILL.md, Phase 0 architecture lens, node-growth re-ask. |
| INV-237 | The session that authored a change never certifies it adversarially; a release's re-review comes from a fresh session. | SKILL.md, persisting the record, closing paragraph. |
| INV-244 | Each project kind declares the composition axes every surface answers, beyond the baseline set. | stress-lenses, delivery separability. |
| INV-248 | For an owed axis that adds runtime code, the design states either how delivery splits along it or why it ships whole; an unexamined monolith is the finding. | stress-lenses, delivery separability. |
| M-6 | A push runs a fresh review pass over the document and the architecture, applies every defect first, and lands a dated record; a push with no matching record should not have happened. | SKILL.md, "the pre-merge check" in the defect kind, and the design-review keying list. |
| E-17 | A prototype artifact carries a visible label, sits in its own home, and nothing reaches the reader as product until its surface has gone through the process. | stress-lenses, unbacked surfaces and unlabelled sketches. |
| C-1 | The baseline axes every stateful surface answers: view, mode, user tier, viewport, reopen, two writers at once, and every co-present surface. | stress-lenses, unwritten seams, the axis list. |
| P9 | Every cross-cutting law owes a test row on each surface it governs. | stress-lenses, declared cross-cutting laws, second demand. |
| base rule 13 | A claim about the shipped system rests on a primary source: a `file:line` you resolved or a command's output you ran. Prose and summaries are leads to verify. | SKILL.md, Meta rules. |
| base rule 14 | A found defect is a sample of its class: name the pattern, sweep every surface for siblings, and fix them in the same change. | stress-lenses, the class lens. |

## Codes that carried no instruction into this edition

| Code | Why it is absent |
|---|---|
| INV-233's counter script | The original names a script in its own repository that counts nodes per file and fails on any increase. This edition states the count and the ceiling as something the reviewer records, since no script travels with the skill. |
| The queued token-comparison script | The original names a row on its own backlog holding the wish for a script that produces the token comparison. No script ships either way, so this edition states the comparison as work the reviewer produces by hand. |
| T-16 | Cited by the neighbouring publish and base skills rather than by this one. It classifies each work item as product, infra, skill, or prose, and this review needs no such classification. |
