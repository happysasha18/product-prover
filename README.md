# product-prover

**A senior-architect review of your product spec — through the lens of [formal verification](https://en.wikipedia.org/wiki/Formal_verification). A [Claude Code](https://claude.com/claude-code) skill.**

Point it at a PRD, feature spec, HLD, LLD, or design proposal, and it reviews the document the way a principal architect would: a short opening assessment, the structural model it extracted, the gaps that matter most, and what to fix before you build.

It thinks in formal-verification primitives — entities, states, transitions, invariants, safety, liveness, atomicity, composition — but it **never lectures you in jargon.** The framework stays private; what you get back is in operational terms you can act on.

---

## The rule it won't break

> Never produce a finding the reader can't trace back to the document.

Every finding quotes the source and pins its location. Every consequence is concrete — *who* is affected, *what* triggers the failure, *what* goes wrong, *what they see* — not "this could be a problem." Every proposed fix is a specific artifact or decision; vague verbs (`define`, `ensure`, `handle`, `consider`) are banned. When the doc is too vague to support a concrete consequence, it says so plainly — *"the spec needs to state X"* — instead of inventing one.

Same instinct as its siblings **[livespec](https://github.com/happysasha18/livespec)** (the full method, packaged — product-prover is its review step, shipped there as a synced copy; this repo stays the canonical standalone home) and **[track-coach](https://github.com/happysasha18/track-coach)**: facts over plausible fiction, and the decision always stays with the author.

It is the reviewing half of a pair — **[spec-author](https://github.com/happysasha18/spec-author)** writes the spec; product-prover reviews it.

---

## What it does

A continuous, structured pass — no pausing between phases:

- **Triage** — is this even an analyzable spec, or marketing copy? Says so up front.
- **Opening assessment** — the 30-second verdict: what it's trying to do, what's working, what needs attention, how close it is to buildable.
- **The model** — extracts entities, states + transitions, actors, and composition boundaries. Tells you exactly **what it assumed** where the doc was ambiguous.
- **Structural issues** — incomplete state space, undefined actors, components mixing roles, abstraction problems.
- **Property analysis** — safety (invariants, pre/postconditions, atomicity, rollback), liveness (dead-ends, termination, silent failure masking), enforceability, and internal consistency — plus generative stress-testing against a set of stress-test lenses — habits of attention, not a checklist.
- **Acknowledged gaps** — the Open Items and TBDs the doc already flags, kept separate so you see what you *missed* first.
- **Human + operational factors** — observability, cognitive load, debuggability.
- **Closing summary** — top 3 things to fix, properties to state explicitly (phrased so you can paste them straight in), and the genuine open questions only you can answer.
- **Two depths** — a full whole-spec pass, or a focused cross-link pass for a single added surface; the depth is chosen per change.
- **Persisted findings** — findings are written to a dated file with a resolved/rejected column, so the next review starts from the last one's open rows.
- **Shipped-system triage** — for a system already in production, a Phase 0 reconciliation note flags where spec claims may not yet match the code, so findings are properly conditioned on what's actually shipped.

Findings come tagged `severity · plain-label (formal-term)` — `must-fix`, `should-clarify`, or `worth-considering` — with severity reflecting real production impact, not formal imperfection.

---

## What's inside

No code, no dependencies, nothing to build or install — product-prover is a single `SKILL.md`: a structured set of review instructions Claude follows. Drop it in, point Claude at a spec, read the findings. Works anywhere Claude Code runs.

---

## Usage

This is a **Claude Code skill** — drop the folder into `~/.claude/skills/product-prover/` and just ask:

> *"review this spec"* · *"poke holes in this design"* · *"is this PRD ready / what did I miss?"* · *"Product Prover this"*

It also has a **glossary mode** — `/glossary liveness`, `/define atomicity`, or just *"what does composition mean?"* — for the formal terms, each with a plain definition, an example, and the question it prompts in a review.

---

## License

[MIT](LICENSE) © Alexander Abramovich.
