# Code lenses — the code mode of the review

This file holds the procedure Code mode calls out to in `SKILL.md`. Read it once Phase 0 has routed
the input here, in place of `reference/stress-lenses.md`.

Code mode runs where no document exists for the code under review: a source directory, a family of
sibling scripts, or a diff with no accompanying spec. Where a document does exist for the code, the
ordinary document pass runs instead, and this file stands down.

## What it reads

No document. Instead:

- **the code itself** — the files or paths named, or the whole directory where none is named;
- **code-derived closed sets** — a set the code's own structure declares, rather than a set a spec's
  prose enumerates. Three shapes: an enum or union type and the switch or match statement that must
  cover every member; an interface or abstract base and the roster of things that implement it; a
  family of sibling files that are supposed to mirror each other's shape, such as parallel installer
  scripts, parallel request handlers, or parallel config schemas;
- **sibling groups** — files, functions, or blocks that share one role: the same kind of thing done
  in more than one place in the tree;
- **a diff**, where one is under review instead of a whole tree — the changed hunks, read against the
  unchanged code around them and against their siblings elsewhere in the tree.

## The two lenses, in code terms

**1. Class-based defect analysis** carries over unchanged. A defect found at one spot is a sample of
its class, the same move the document pass's class lens makes. Three questions:

- does the same mistake live elsewhere in the code?
- is there an architectural cause — a boundary drawn wrong, or a pattern with no shared
  implementation — that lets the mistake recur instead of being caught once and fixed everywhere?
- does the test suite cover this class of mistake, anywhere in the tree it could occur, or only at
  the one spot where it happened to be caught?

**Sibling-defect search** is the mechanical half of this same lens, not a second lens standing beside
it. It is how "does the same mistake live elsewhere" gets answered concretely, in code:

- **exact-pattern grep** — search the tree for the literal broken shape: the missing arm, the
  omitted check, the un-handled case, wherever the same tokens recur;
- **family walk** — find every file that plays the same role as the broken one (the rest of an
  installer family, the rest of a handler family, the rest of a config-loader family) and read each
  one for the same defect;
- **sibling diff** — diff the broken file against its closest sibling in the family. A defect often
  shows up as the one place the diff isn't empty where it should be;
- **caller walk** — find every caller of the broken function or script, and check whether each call
  site depends on the behaviour the defect breaks.

**2. Completeness-of-sets checking** carries over with what "the set" is built from now different.
In a document, the set is a spec's own prose registry — an enumerated list the author wrote out. In
code, the set is the code's own structure: an enum or union matched by a switch or match statement,
an interface's roster of implementers, or a family of files meant to mirror each other. This reframes
as **closed-set completeness**: for every closed set the code declares, is every member handled the
same way, and where one member is handled differently, does the code say why?

## Finding format

A code mode finding keeps the four-part shape from "How to write findings" in `SKILL.md` — headline,
source, consequence, fix — and the same `kind · plain-label (formal-term)` tag, with one change.

**Part 2 — Source.** Cite `path:line` instead of a document quote and section: `scripts/foo.sh:23-28`.
Quote the exact line or lines, not a paraphrase. Where the finding spans a family of files, cite the
one line in each sibling that carries the pattern, or its absence.

## What does NOT transfer without a document

Four capabilities from the document pass stay out of code mode, because each one needs a document to
check the code against:

- **declared cross-cutting laws** — the sweep reads a document's own section naming its laws and
  their enforcers. Code alone states no law for the review to check compliance against.
- **lifecycle sweeps** — judging whether a default, a fallback, or a terminal state is correct needs
  a stated intent to compare the code's behaviour to. Code alone shows what a state machine does, not
  what it was supposed to do.
- **provisional defaults** — the `[default]` mark exists to flag an unratified sentence written into
  a document, standing until its owner confirms it. Code carries no such sentence, and no author
  intent recorded beside a value for this pass to flag as pending confirmation.
- **three-source disagreement** — that lens reads a document, an architecture, and the code together,
  and names where the three disagree. With no document, two of the three sources are gone, and the
  lens has nothing left to triangulate against.

Name these four as out of scope in the record, rather than silently skipping them.
