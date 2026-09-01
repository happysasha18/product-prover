# How product-prover works

The skill never says "formal verification" anywhere you'd read it. Tell a model it's an expert in something and it starts sounding like one — jargon, definitions, a lecture where a review was wanted. The vocabulary shapes how it looks for gaps, then stays behind in the tag at the end of each finding: `defect · no-exit (dead-end)`. What actually does the work is duller and stricter — a finding must name who is affected, what triggers it, what breaks, and what state it leaves behind; a proposed fix is rejected if it says *define*, *ensure*, or *handle* instead of naming the thing to change.

## Does this fit your document?

It works from entities, states, transitions, invariants, preconditions, atomicity, and liveness — a document's genre decides nothing. Protocol and API designs, workflow and approval flows, permission models, migration plans, failure runbooks, firmware state machines, and architecture documents all qualify. Two constraints are hard. It needs a written document, or, where none exists, code mode's own narrower ground: a source directory, a family of sibling scripts, or a diff, with no diagram-in-your-head substitute for either. And the document has to claim behaviour: point it at a vision deck and triage says so up front.

The method assumes no product kind. Every sweep and every lens states its reading in terms. Those terms hold for a backend service, a protocol, a library, a data pipeline, a command-line tool, or a screen. Where a reading needs a concrete instance to be understood, it gives two or three from different kinds. A guarantee's condition band reads as a viewport range on one document and as a payload size on the next. The state carried across a transition is focus and scroll position in one document, and an open lease or a half-filled buffer in another. Product specs are where it has been used most, and that shows in the vocabulary of its output alone.

It finds holes in what a document *claims*, and your test suite proves what the artifact *does*. Applying a fix, rejecting it, and settling a judgment call stay with you. Market fit, pricing, and whether the feature is worth building are outside it.

## What sits beside it

Two more passes belong beside this one, and are left to their own reviewer. One is whether a stranger can read the prose. The other is whether the design itself is right. Both ship in [live-spec](https://github.com/happysasha18/live-spec), the fuller method this skill was lifted from. It wires this review to a spec author, a test author, and a set of mechanical gates.

Problems go to [github.com/happysasha18/product-prover/issues](https://github.com/happysasha18/product-prover/issues), and a gap it missed on your own document is the most valuable report to send.
