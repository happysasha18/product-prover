# The architecture lens — Phase 3e, armed by Phase 0

Phase 0 arms this lens when the input is an architecture document. Read this file once that
happens, in place of writing the lens from memory, the same way a full pass opens
`reference/stress-lenses.md` before the rest of Phase 3e.

---

**The architecture lens.** Phase 0 arms this lens when the input is an architecture document, and its
seven checks run here, beside the mandatory sweeps. Each check is judged at the scale the project's
own kind sets. The project states its kind in a few words. Examples: a backend service, a static site,
a fullstack app, a command-line tool, and a mobile app. Others: a library, a data pipeline, a skill
pack, or a book. Any other kind is stated the same way. The kind decides the form each check can
demand, so a skill pack and a backend service answer the placement check differently. The seven
checks:

- Every fact the requirements document states is owned by exactly one node.
- No node stands without backing in the requirements. A node with one caller and no promised second
  is flagged as speculative. It waits for an answer: a named plan that turns it into a yes, or
  a merge back into its caller. Three questions decide whether a node stands on its own. Can it be
  tested by itself? Does a real second place need it? Can it and its neighbour be worked on at the
  same time without queuing on the same files? One "no" calls for an answer before the node stands,
  and the speculative-node case above is one of those. Two or more reads the node as premature.
- Every seam names what crosses it and which side owns the format.
- The quality budgets are stated with the place each number is measured, and each names its
  watcher. The watcher is the mechanical check that fails past the stated number. A decided
  sentence naming why a person reads a budget by eye is the other form the watcher takes.
- The runtime view walks every flow the requirements promise.
- The placement view says where every node runs, with its load-bearing technology where one exists.
- The node-growth re-ask. Each node re-answers the three fitness questions on its pins as they
  stand now, because a node born right and then grown carries a standing yes nobody re-reads.
  Co-residence in one file is the mechanical face of a failed growth answer. Read the node count
  per file from this document's own pin column, counting the distinct nodes whose pins name a
  file. Raw file size is the wrong signal for this. A file holding more than one node is read for
  whether its co-resident nodes each still earn their place. Record the per-file node counts with
  the review. That count is a ceiling: the next review reads any file whose count rose as a question
  about what grew. A split moves through the architecture step and its re-review.

Every pin is a real `file:line` citation, and a prose description fails that bar. The paired
requirements document must be in view, because ownership is checkable only against the fact list it
owns. Where no such document exists, ask the author for it. Where none can be produced, record
the ownership check as not runnable with that reason, and run the remaining six.

This lens writes a finding the way every other lens does: the four-part format, with the architecture
document's own section as the source pin in Part 2. Each of the seven checks also owes one verdict
line, reading hit, clean, or N/A with its reason — the same three verdict words the mandatory sweeps
write. The seven lines stand together beneath the class line, each naming its check, and the per-file
node counts stand beneath the node-growth line.
