# Stress lenses — Phase 3e of the review

This file holds the two tiers of generative stress-testing the main pass calls for in Phase 3e. Read
it at that point in the review.

Stress-test every operation, transition, rule, and assumption against the families of questions
below. The specific cases are yours to invent, from what the operation actually does.

Two tiers live here:

- **Mandatory sweeps** run on every full review. Each owes one verdict line in the persisted record,
  reading hit, clean, or N/A with its reason. A missing verdict line reads as a skipped sweep, and it
  never reads as a clean one. The record renders those verdicts as the surface × sweep table.
- **Imaginative probes** are habits of attention. No checklist ticks them off, and no verdict is
  owed.

A lens that prompts no real concern produces no finding. Inventing an issue to satisfy a lens is
forbidden.

---

## Mandatory sweeps

### 1. Declared cross-cutting laws

Read the document's declared-laws section. That is the one place naming the laws that cut across
every surface: measurement, accessibility, error handling, a register of language. Each declared law
carries the three demands below, and an unmet demand is a broken-invariant finding.

Recognize that section by what it holds, since no heading is prescribed for it. It is one section of
the document under review listing the laws that hold everywhere, each named beside the thing that
catches a violation. Any of these is that section: one headed "Cross-cutting requirements", one
headed "Global rules", or a requirement declaring three such laws with their gates. Read for that
content rather than for a title.

A document with no place where its cross-cutting laws are declared earns one finding naming that, and
the per-law walk starts once that section exists.

Where the document's author writes each section's clause as they go, this sweep audits the clause the
author already wrote.

- **A clause per surface.** Enumerate every surface and transition, and demand the law's clause or a
  dated exemption on each. A missing clause ranks as a broken invariant.
- **A test per surface.** Demand a test row on each surface the law governs. A law stated everywhere
  and tested nowhere is a finding of the untested-surface class. Where the project runs a mechanical
  coverage check over its test matrix, that check is the floor and this sweep is its semantic
  reviewer. Where the project runs no such check, this sweep is the only reader, and say so in the
  verdict line.
- **A named enforcer.** Every declared law names the thing that fails when the law is broken, and
  this demand reads the enforcer recorded beside the law. Three enforcers qualify:

  - a mechanical gate: a named script or a dedicated test, deterministic and blocking in continuous
    integration. Use this where a deterministic check can decide the violation;
  - this review itself, where the violation pins to a stated sentence and the review blocks;
  - a design-consistency review's recommendation, which is soft, because the deciding fact lives in
    the author's intent alone.

  A law with no named enforcer ranks as a broken invariant.

### 2. Edge-condition completeness

The mechanical face of the bounds and dependency probes, run as a completeness sweep across every
case. Five checks:

- **Range ends.** Find every transition the document gates on a quantity that runs on a line: elapsed
  time, a count, a distance, a size. Assert that each one names its behaviour at both ends of the
  range. The reader then learns what holds below the low end and above the high end. A clause like
  "on return", "after a while", "once there are several", or "when it gets large" names one point. It
  leaves an unbounded interval silent. That silence is the finding, of the blank-answer class: a
  reachable situation the document leaves unanswered.
- **Async pending, arrived, failed.** Find every piece of content the document produces
  asynchronously into a place already reserved for it. That place can be a region of a screen, or a
  field a caller polls. It can also be a status record a consumer reads, or a progress line a command
  prints. Assert the document names its
  three states, pending, arrived, and failed, and that the pending state is observable at that place.
  A place that stays blank and silent while its result is in flight is the finding. The author writes each
  edge as a sentence in the document. This review invents no answer, and where only the person who
  owns the decision can judge the timing, it surfaces the question to them.
- **The named-part ask.** A guarantee scoped to a named part of its domain draws the standing
  question about the remainder. That part may be a band of a ranged quantity, a user state, a network
  condition, or a locale. Any named sub-case of the domain it governs counts. Each remaining part
  owes a decided sentence or a sentence marked as a provisional default. A guarantee true as written
  over one part, while the remainder stays silent, falls in the blank-answer class.
- **The condition quantifier.** Every guarantee that depends on a condition of its environment names
  the range of that condition it covers. It either holds across the whole range, or it names the band
  it is scoped to. A band-scoped guarantee draws the standing question about the other bands.
  Three instances: a layout guarantee across viewport sizes, the short-viewport band among them. A
  second: a latency guarantee across payload sizes, the largest among them. A third: a command's
  output guarantee across terminal widths, including output redirected to a file.
- **Same-kind-group handling.** Where the parts are a same-kind group no clause declared, a
  design-consistency review reaches them, and this review holds them once they are declared. A worked
  case: a caption rule scoped to "on a phone" printed over the picture on a rotated phone, which was
  wide and short. A second instance: a retry rule scoped to "on a timeout" that left a connection
  reset unanswered. Every consistency check read clean, because the claim was true as written.

### 3. Cross-surface policy uniformity

A clause sometimes states a policy for an interaction kind that lives on several sibling surfaces.
Four examples: an authentication rule on every endpoint of a family, and a retry policy on every
consumer of a queue. Two more: a flag's meaning on every subcommand, and a gesture policy such as
"browser pinch-zoom is refused" on every screen of a kind. For such a clause, enumerate the surfaces of that kind from the project's surface
registry, the one list it keeps of its surfaces. Then check whether the clause governs every one of them,
or only the surface where the decision was born. Where the project keeps no such list, this sweep
takes an N/A verdict naming that as its reason. The verdict still goes in the record.

A policy written for a single surface while siblings of the same kind exist is a finding. The clause
should name the surface class and enumerate its members, so the policy holds uniformly. This catches
at document time what a test suite asserting only the named surface passes green, while the running
product stays non-uniform. A rendered product also gets a mechanical floor, where a completeness
check asserts the policy on every sibling surface the product exposes.

This sweep is the preventive twin of the class lens below. The class lens sweeps a found defect's
siblings; this one holds a decided policy uniform before any defect is filed. Its discovery-side
sibling is a design-consistency review, which reaches the undeclared same-kind groupings this sweep
stays blind to for want of a declaration. Where a class is already declared, this sweep governs.
Where none is declared, a confirmed grouping from the design review lands here as a class clause the
author writes.

The sweep also fires on a **kind-general rule written in a single member's section**. That is a
sentence stating a principle for a whole kind, homed on one surface while siblings of that kind
exist. The principle may be a way in and out, a naming rule, an error contract, or a gesture. It is the same defect the
moment the kind is recognizable from the sentence itself, before any class is declared. The finding
asks the author to lift the principle to a class clause enumerating its members. The other answer is
to scope it to the one member by a decided sentence. This is the prose form a declared-class
enumeration alone would miss, since that enumeration presupposes the kind is already declared.

### 4. Lifecycle

One surface's whole life across enter, leave, cover, and return. The sub-questions gather under the
transition-payload parent, so the one lifecycle is walked once as a single pass. Five separate angles
would otherwise collide over it. Each sub-question keeps its own anchor.

**Transition payload** — the parent lens that the topology checks all serve without naming: entry
symmetry, dead-end, and scenario entry and exit. For every transition the document states, enumerate
the parameters that carry across it and that the document leaves unsaid. Ask which of them a
platform default silently decides. On a screen: where focus and selection land, what scroll or
playback position holds, whether sound continues. On a service or a job: whether an open connection,
transaction, lease, or cursor survives, and whether a timer keeps running. It also asks whether a
cached value is fresh or stale on the other side.

A parameter the document leaves blank is answered by the platform default alone. A default that
silently becomes the behaviour leaves the topology lenses no written text to catch it by. Each
unstated parameter is a finding, of the blank-answer class.

The paired-transition-symmetry lens and the entry-state lens below are instances of this one. Each reads this lens
on a single payload parameter: an exit's animation, a re-entry's internal state. A worked instance: a
side panel's transition names its opening ceremony and its exit, and leaves scroll position silent.
The platform default, a reset to the top, becomes the behaviour unreviewed. A second instance: a
worker's lease named at acquisition and left silent across a restart, so the runtime's default expiry
becomes the behaviour unreviewed. This lens names the missing parameter, and the entry-state instance
writes its sentence.

**Entry symmetry** — for every state, mode, or view entered under a condition, ask what deliberate
path re-enters it later. The conditions are a first visit, an empty state, onboarding, a one-time
banner, a first-run setup, a degraded mode entered on a dependency failure. A conditionally-entered face with no deliberate re-entry path is a finding. The document
clears it by stating the one-way as a decision, by name. Three trigger patterns give it away: "only
on first visit", "only on first run", "until dismissed". Each such clause owes its return sentence.
The dead-end lens tests states for exits, and this lens tests faces for re-entry over the visit's
lifetime.

**Entry state** — beside entry symmetry above, for every state, mode, or view something can leave and
re-enter, read what state re-entry opens in and whether entering resets it or resumes what a prior
visit left behind. On a screen that reads as focus and scroll position. On a session-bearing service
it reads as the cursor, the cached credentials, and any half-filled buffer. On a command it reads as
the working directory and the saved profile.

A surface sometimes pins its opening ceremony, its exit, its variants, and its guards, while its
entry position and its reset-or-resume semantics stay blank. That surface is a finding, in the
blank-answer class. The author writes the entry state as a sentence in the document. Where only the
person who owns the decision can judge whether entry should reset or resume, surface it to them. Once
the entry state is written down, ordinary state coverage holds it.

Entry symmetry tests that a re-entry path exists, and this tests the state that path opens in. That
is the question entry symmetry leaves unasked. It closes a class the two path lenses missed. A worked
instance: a gallery side panel reopened on the last picture a prior visit had scrolled its lane to. No
line stated that the lane lands on the first member and resets at entry. A twin: a consumer
reconnecting to a stream that resumed at the newest message. No line stated whether it resumes at the
last acknowledged one.

**Paired-transition symmetry** — when a surface states a transition on one direction of a paired
state change (open/close, enter/exit, expand/collapse, show/hide, subscribe/unsubscribe,
acquire/release, register/deregister, start/stop), the opposite direction owes an
answer too. Symmetry is the default, and a written reason is what parts the pair. Four reads follow,
and a missing answer in any of them is a blank-answer finding. Where the pair's quality is a taste
call, the open question is surfaced to the decision-owner. It is marked as a provisional default, and
it holds nothing back. Motion feel on a screen and backoff length on a service are two such taste
calls.

This is the temporal twin of the cross-surface uniformity sweep above.

- *The transition* — one direction described, the other silent. The exit owes a written answer: a
  mirror, a named shorter exit, or a deliberately instant one. A blank fails this read.
- *The inverse of the means* — a state entered by a particular means owes that means reversed among
  its stated ways to leave. Three examples exist. A pinch, drag, or lift is undone by the same
  gesture. A subscription is closed on the channel that opened it. A lock is released by whoever took
  it. A decided sentence for its absence answers the read as well.
- *The inverse's magnitude* — where the pair rides a continuous quantity, such as a pinch span, a
  drag distance, a wheel accumulation, a backoff interval, or a batch size, the document owes an
  answer on the inverse's size. The
  question is whether the inverse demands the same magnitude as the forward move. The answer is
  symmetry, or a named deliberate asymmetry.
- *Kind* — a declared one-sided pair is a `defect`, since a required answer is missing. A
  never-declared same-kind grouping over the same gap belongs to a design-consistency
  review's parity check, which recommends.

**Persistence and versions** — the system sometimes persists state beyond the session, in local
storage, files, caches, or saved preferences. What happens when state written by an older version
meets the current code and interface? Is the stored shape partial, orphaned by a removed feature, or
read on reopen into an interface or a schema that no longer matches it? Is there a defined migrate,
ignore, or clear rule? This is the family of a saved preference restored into a changed interface. It
is also the family of a record written out earlier and read by code whose schema moved on.

**Scenario entry and exit** — a scenario is a flow, such as "walking the gallery",
"answering the quiz", "when a bug cuts the line", "processing a nightly batch", or "recovering from a
failed migration". For every one of them, check that the document
states how it is entered and how it exits. The entry names which prior scenario or state it comes
from, and what is already true, meaning the preconditions the walk assumes. The exit names where the
person lands, and what the flow leaves true for the next scenario, meaning the postcondition.

A flow whose entry or exit is unstated is a finding, of the same blank-answer class. This is the
per-operation precondition and postcondition lenses lifted to the scenario level. It is akin to the
entry symmetry lens, which tests a face's re-entry while this tests a whole flow's edges. It is akin
to the runtime view's flow walks as well.

A trivially-none edge stated as such is a decided answer: a top-level scenario entered from nowhere,
a terminal one exiting to nowhere. A silent edge is the gap. The duty binds forward. Flag an existing
scenario's unstated edge as a finding, and leave the current change free of the backlog older
scenarios never wrote.

**The boundary lines**, so a reviewer who ran one sub-question knows what it left uncovered:

- the reopen case belongs to *entry state*, as the re-entry transition's payload, while *persistence
  and versions* covers a stored shape meeting newer code;
- *entry symmetry* tests that a re-entry path exists, and *entry state* tests the state that path
  opens into;
- motion across the pair and the inverse of the means belong to *paired-transition symmetry*;
- a whole flow's edges belong to *scenario entry and exit*.

### 5. Unwritten seams

For every stateful surface, derive the reachable situations yourself and check each one for a written
answer. The axes the author remembered to fill are the starting point, and the walk carries past
them.

Walk every axis the surface passes through while it is already active. Those axes are view, mode,
user tier, version, the environment band it runs in, re-entry, and two writers acting on it at once.
A relayout
when the window changes shape re-runs an entry animation nobody composed. A second instance: a config
reload while a request is in flight leaves that request on the old values with nothing stating so.

Then walk the axis authors forget most: every other surface that can be present at the same time.
Those are the things present alongside it. Three examples: the siblings on the same screen, the other
consumers on the same queue, and the neighbouring stage of the same pipeline. The list also includes
the surface one step before and one step after it in the flow. That other surface counts whether or
not it holds state of its own, and a
static end screen counts.

For each situation ask one question: is this surface's behaviour stated while that other one is
present, or through that change? A reachable situation with a blank answer is a finding, of the same
class as a fact no part of the architecture owns. It is a state the document leaves out while the
running product still reaches it.

Report the situational seam the document left blank. This review invents no answer and asks the decision-owner nothing. The
author writes the sentence as a composition invariant, decided or marked as a provisional default.

---

## Imaginative probes

- **Ambiguity and ties** — when the document selects, ranks, matches, or chooses, what if inputs are
  equivalent on the criterion? Is the resolution deterministic?
- **Concurrency and order** — when actions happen in sequence or parallel, what if they overlap,
  repeat, or arrive out of expected order?
- **Bounds and edges** — when the document assumes ranges, limits, or quantities, what happens at the
  boundaries, absence among them: zero, missing, none?
- **Dependency reality** — when the document relies on something external, what if it is unavailable,
  delayed, or returns something unexpected?
- **Reference integrity** — when the document uses identifiers or pointers, what if the referent is
  missing, has changed, or is shared?
- **Surface authority** — when an operation creates, modifies, or removes an object of some category,
  ask whether another component should be the authoritative management surface for that category. The
  document either mentions that component or implies it. Where one exists, ask whether this operation
  publishes to it, registers with it, or otherwise keeps that authoritative surface complete.

  File a finding only where the document itself gives clear evidence of a competing authoritative
  surface. Speculating about phantom components, and assuming authorities the document never states,
  both stay out.

  Where the document names no authoritative surface for the category, write a stated assumption
  rather than staying silent. The assumption line reads:

  > I found no authoritative surface for <category> named in this doc. If one exists in the product,
  > this operation does not register with it.

  The line goes into the What-I-assumed lines, and it stays out of the findings. It costs nothing
  when it is wrong, and it catches the author who forgot the registry entirely. That is the case a
  clear-evidence gate self-disarms on. Where an architecture document is also in view, the
  three-source lens below supplies the missing evidence. That document names the authoritative
  surfaces the document under review omits.
- **Class lens** — when a lens above, or any phase, surfaces a defect at one spot, treat it as a
  sample of a class. Three questions come before the finding is written:

  - *Does the same kind live elsewhere?* Sweep the whole document for the same pattern in every other
    section and surface: the same wording, the same structure, the same omission. Write one finding
    that names the class and lists every instance found. A point finding on a class defect sends the
    author on the sweep the pass skipped.
  - *Does the architecture account for the defect's cause?* A boundary drawn wrong, or left silent,
    can let the class exist. A structural cause is a finding against the architecture document
    itself, and it reaches past the single instance.
  - *Does the document describe the broken behaviour at all?* A document silent on it, or
    under-describing its composition, is the real defect the finding names, and the fix to the
    document comes before the fix to the code. This review catches nothing the document never states.
- **Interactive overlap across layers** — two things can sometimes take the same input at the same
  time. Four examples follow: one surface open over another while the lower layer's controls stay
  live, and two routes matching one request. Two more: two consumers on one topic, and two key
  bindings claiming one key. Ask whether the document states which one receives the input and what
  happens to the others.

  One worked instance: one surface opens over another, as a modal, a zoom, or an overlay, and the
  covering surface carries its own controls. Read the document for every other interactive control
  that stays on screen while the overlay stands. Ask whether the document states that control is
  hidden or made unpressable.

  A document that opens one surface over another and leaves the lower layer's controls unanswered is
  a finding, in the blank-answer class. The covering surface should retract the lower layer's
  controls, hiding them or setting them unpressable, so every press lands on one control alone. A
  passive element may overlap freely: a caption, a plaque, the artwork. The rule binds whatever can
  take input.

  An ordinary test suite stays green while the running product collides. An assertion at the level
  where the collision happens is the floor. A browser check and a route-table check are two such
  assertions. This lens catches the blind spot earlier, reading the document's layered surfaces.
- **Unbacked surfaces and unlabelled sketches** — when the document, or the build it describes,
  exposes a user-facing surface, ask whether a clause backs it. Three shapes are the finding:

  - a surface the document marks as planned or "not yet specified" that exists in the build anyway;
  - an exploratory sketch wired into or linked from a production surface;
  - anything shown to a person as product without having gone through the document.

  The build carries only what the document names. This is the family of "the hand-built room shown as
  if shipped". A prototype earns its own visible label, lives in its own home, and nothing in the
  shipped product reaches into it.
- **Approved-look clauses** — when a clause encodes an approved exemplar, meaning an artifact somebody
  approved as the norm: a prototype, a reference response, a golden output file, read it twice. Does it point at the frozen copy of that approved artifact?
  Does the clause's text contradict its own artifact, as prose demanding a question the approved
  design answers wordlessly? A prototype-born clause with no pointer is a finding, and so is clause
  text contradicting its own artifact. The pointer cites a frozen dated copy. A pointer into a
  live prototype directory fails this read, since the artifact it names can change under the clause.
- **Three-source disagreement** — read the change against the document, the architecture, and the
  code together, and name where they disagree. Three shapes are the finding, and each one routes to
  the home that owns it:

  - a surface the document promises with no owning part of the architecture, which routes a
    restructure item for the missing part;
  - a behaviour in the code no clause backs, which routes a bug item;
  - a part of the architecture pinned to a line that moved, which routes a fix to the document.

  One source is never picked as the winner in silence. This pulls the reconciliation of document
  against code forward to intake. Drift then surfaces as a finding at entry, caught before it becomes
  a surprise at code time. It is akin to the unwritten-seam sweep, where a drift with no routed home is
  itself the finding. It is also the read that tells whether an already-proven artifact settles a
  question. Where it does, a reviewer derives the answer directly, and raises no fork.

  When the disagreement is a product-versus-document divergence, the document is the definition of
  correct. The divergence defaults to a possible error in the product, checked against the document.
  Changing the document is a decision its owner ratifies after understanding the divergence, and it
  is never a silent rewrite to match the product.
- **False serialization and over-broad independence** — the document under review is sometimes a
  concurrency plan. Three examples: a sprint board, a set of parallel work streams, and a task
  dependency graph. Read every serialization it declares and every edge it draws. Two findings live
  here, one per side of the edge rule.

  On one side, a plan that serializes two movements on shared-document co-location alone is a
  finding. Both movements land in the spec, the architecture, or the test matrix and share nothing
  more. Those shared documents are reconciled when the work is integrated, so two items that share
  only a document still open in parallel. The same finding covers two more shapes. One is an edge
  drawn where no movement needs another's finished output. The other is a same-section or
  same-behaviour collision, where the two rewrite one clause or one behaviour's rule.

  On the other side stands the safety twin, a finding of equal weight. Two items that truly collide,
  through a real dependency or a same-section rewrite, are marked independent and opened in parallel.

  This lens stays a senior read. A mechanical gate keyed on it would fail every lawful change, since
  every movement lands in the shared documents. Judging a false edge or a false independence reads the
  graph itself, and a diff cannot make that call.
- **Delivery separability along a declared axis** — the document under review sometimes declares a
  cross-cutting composition axis that adds runtime code: an input capability, an assistant capability
  on or off, a rendering engine, a viewport tier. Read the delivered artifact against that axis. Does
  what the consumer receives divide along the axis, or ship as one piece? The composition question asks
  whether behaviour splits along the axis. Its dual reads whether the artifact the consumer receives
  divides along the same axis or arrives whole.

  The finding is an unexamined monolith: an axis adding runtime code whose design names no stated
  architectural reason to ship whole. It also names no delivery road it owes. A stated reason reads as one
  bundle, one page never torn down, a no-server delivery, or a payload too small for a split to pay. A
  delivery road reads as a platform split, a lazy load, or a per-value chunk carried by a later item.
  A monolith named with its reason is a settled answer and no finding. Byte weight is the symptom, and
  the unasked separability question is the root.

  The lens generalizes past input capability to any owed axis, each one only where covering that axis
  ships runtime code. A viewport answered by a media query, and a locale answered by a logical
  property, add none, so the lens stays silent there. It stays a senior read, like the edge lens
  above. A named-reason monolith is lawful, so judging an examined choice against an unexamined one
  reads the design's own reason. A diff makes no such call.

  This lens was itself found as the dual of the composition law it enforces. That pairing is a
  standing discovery habit. For a lens this list applies, ask whether that lens's dual bites the
  document. Safety pairs with liveness, state with transition, and atomicity with isolation.

  The habit surfaces a lens the list is missing, and it never demands every lens ship a partner. Some
  duals collapse into a lens already run: an invariant's dual is its decreasing progress measure, which
  the liveness reading already covers. Some others are nameable and rarely bite.
