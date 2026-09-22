# product-prover

A [Claude Code](https://claude.com/claude-code) skill that reads a spec, architecture document, or codebase and finds the structural gaps a normal review misses — the state with no exit, the operation that isn't atomic, the promise the code can't keep.

## What you get

A reviewer only catches errors the document gives them words for. A missing rollback, a state with no exit, an operation that isn't atomic — these have no words on the page to argue with, so nobody argues, and the spec passes.

That used to be survivable: a human had to build from the document, and a person building against a hole produces friction — a question in grooming, a spike, an argument. An agent generating from the same document produces none. It fills the hole with a plausible default and keeps going, and the tests get derived from the same document, so they say nothing about the missing property either.

Green suite, shipped gap. The review has to happen on the document, before anything is generated from it.

## An example finding

Run against a parcel-locker spec, the skill returns findings like this — a quote from the document, what actually breaks, and a concrete fix:

> **F1 — Expiry permanently consumes a compartment**
>
> *"The expiry sweep ... moves every parcel whose pickup window has run out into Expired."* — Section 7
>
> A bank operator reaches the next morning with an Expired parcel still occupying its box. No actor, deadline, or transition returns it to the carrier, and neither expiry nor return makes the compartment free. Each expiry therefore reduces the bank's usable capacity until somebody performs an undocumented repair.
>
> Add a `Returned` state, name the actor and deadline for the return, and make that transition free the compartment.
>
> `defect · no-exit (dead-end)`

Full run on the same spec, ten findings and a compact model of the whole document: [`examples/sample-response.md`](examples/sample-response.md).

## Article demonstration

The deliberately incomplete parcel-locker input and its full historical Product Prover v4.3.0
review, used in [*Prose as Code: Applying Formal Verification to Product Specs*](https://alexanderabramovich.medium.com/prose-as-code-applying-formal-verification-to-product-specs-14f04fee8f2d?source=friends_link&sk=e293d19e7adcd1126c593219e22cf7e3), live in
[`examples/parcel-locker-article-demo/`](examples/parcel-locker-article-demo/). It is an
explanatory artifact, not this release's canonical sample or test fixture.

The current regression set pairs a deliberately flawed Parcel spec with a repaired control and an
explicitly ordered negative control in
[`examples/parcel-locker-witness-eval/`](examples/parcel-locker-witness-eval/). Its independent
release readout is [`evals/release-1.7.0.md`](evals/release-1.7.0.md).

## How the logic works

The skill never says "formal verification" anywhere you'd read it — the vocabulary shapes how it looks for gaps, then stays behind in the tag at the end of each finding. Mandatory sweeps and open-ended probes run against the document. When a suspected gap depends on replay, competing rules, a component boundary, or eventual progress, a small behavioral witness tests it before it becomes a finding. The class lens stands beside them, and it owes a line of its own. Its move: a defect found at one spot is swept across the document for its look-alikes. Each pass records whether that sweep ran. What it actually checks and why: **[the full explanation, with the lenses and what each one catches →](docs/how-it-works.md)**

## Does this fit your document?

It works from entities, states, transitions, invariants, preconditions, atomicity, and liveness — a document's genre decides nothing. Protocol and API designs, workflow and approval flows, permission models, migration plans, failure runbooks, firmware state machines, and architecture documents all qualify. Two constraints are hard: it needs a written document (or, with none, code mode's own narrower ground — a source directory, a family of sibling scripts, a diff), and the document has to claim behaviour — point it at a vision deck and triage says so up front.

It finds holes in what a document *claims*; your test suite proves what the artifact *does*. Applying a fix, rejecting it, and settling a judgment call stay with you.

## Use it

Point it at a spec, an architecture document, or — with no document at all — a codebase, and ask for a review:

> *"review this spec"* · *"does this architecture hold together?"* · *"run product-prover on this"*

## Install

Claude Code required. Two items copied into your skills directory:

```bash
git clone https://github.com/happysasha18/product-prover.git
cd product-prover
mkdir -p ~/.claude/skills/product-prover
cp -R SKILL.md reference ~/.claude/skills/product-prover/
```

This repo is the canonical source. The [live-spec](https://github.com/happysasha18/live-spec) pack installs the same files as one of its skills — a pack install and a direct install land identical content.

## Known issues, release history

[`docs/known-issues.md`](docs/known-issues.md) · [`CHANGELOG.md`](CHANGELOG.md)

---

[MIT](LICENSE) © Alexander Abramovich. The skill is prose, so it pulls in no third-party code and carries no dependency of its own. The sample spec is written for this repository and describes no real company. This is release `1.7.0`, and this repository's version line is the only one the skill follows.

---

grown in [live-spec](https://github.com/happysasha18/live-spec) · standing on its own since 1.0.0
