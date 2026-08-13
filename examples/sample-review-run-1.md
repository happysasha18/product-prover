# Product Prover review record — Cedarline Lockers, release 2

- **Skill:** product-prover, edition `1.0.0-standalone` (as `metadata.version` in `SKILL.md` states it)
- **Date:** 2026-08-06
- **Document reviewed:** `editions/product-prover/examples/sample-spec.md` — "Cedarline Lockers — parcel pickup, release 2 (sample spec)"
- **Mode:** full review (the default; nobody named another mode)
- **Record scope:** review only. No fix was applied to the document, and the finding ledger's status column says so on every row.

### What this project does not have

Several rules in this skill name a check the reviewed project may or may not run. This pass was
instructed to read the skill, its reference page, and the sample document alone, so nothing about the
surrounding project was inspected. Four rules therefore read as advice here, and none of them ran:

- a pre-merge check that applies defects — not verified; every defect below stays open;
- a test suite — not verified, so the "a test per surface" demand of the cross-cutting sweep was read
  by this reviewer alone, with no mechanical coverage floor under it;
- a readability review — not run; comprehension stops and undefined terms are out of this pass;
- a design-consistency review — not run; the undeclared same-kind groupings stay unreached, and the
  places where one would help are named below.

The **surface registry** — the one list the project keeps of its surfaces — does not exist for this
document. Where a sweep reads it, the verdict is N/A with that reason, and the sweep still appears in
the table.

The **merge-delta gate** stands down by name: no old side of a rewrite is in reach, so this pass
reads the document as it stands.

---

## Phase 0 — Triage

`TRIAGE: PROCEED` — this is a feature spec for release 2 of a physical parcel-locker service. It
carries actors, entities, a four-state parcel lifecycle, three operational flows, stated rules, and
non-functional claims. There is more than enough to extract a model from.

Three triage notes:

- **Does the document claim to describe a shipped system?** Partly. Section 1 says release 2 "adds the
  pickup window and the expiry sweep to the release 1 deposit flow", so the deposit path, the actors,
  and the entity set are claimed as already built. The document carries no pins: no surface names a
  `file:line` that holds it. The code is out of reach altogether for this pass — the instruction for
  this run was to read the document alone. **Every finding touching the release 1 deposit path is
  therefore conditional on the document being current.** That covers F1–F6, F9–F11, F15, F20, F22 and
  F31. If a section describes a surface no code owns any more, this pass cannot tell, and a spec that
  outran a deletion would "prove" dead behaviour.
- **Is the input an architecture document?** No. It states no nodes, no placement, no runtime view.
  The architecture lens and its seven checks do not apply, and no per-file node count is recorded.
- **Product kind, in a few words:** a networked physical-device service — locker banks in the field,
  a central Cedarline side, and one third-party gateway. That kind sets the scale for what each check
  can demand, and it is why offline behaviour and irreversible physical acts weigh heavily below.

## Opening assessment

This spec describes a parcel-locker service where a courier deposits into a compartment, a code
travels to the recipient by SMS, and an unclaimed parcel is swept into an expired state after a
pickup window. Two things are working well. The state list in Section 4 is honest about what each
state means and when it is entered, which is exactly the shape a reviewer can argue with — most specs
at this stage name states and skip the entry conditions. And Section 13 declares its own open items
instead of burying them, including the capacity question that half the flows below depend on. Two
things need attention before anything is built. First, the document contradicts itself in five
places, and each contradiction is between two clauses that are individually reasonable: the pickup
window is 72 hours and the sweep that ends it runs once a day; only the recipient may open a
compartment and an operator may open any; a bank works offline and every deposit needs the central
side. Second, the physical world is irreversible and the document treats deposit and pickup as single
sentences — the courier shuts a door, and four system steps follow with no failure behaviour written
between them. Overall confidence: **needs another iteration**. The model is close enough that a
focused pass over the contradictions, the deposit atomicity, and the Expired dead end would get it to
buildable; nothing here calls for a rework of the design's shape.

---

## Phase 1 — The model

No diagram is rendered. This review is written into a file, which is an environment that renders no
visuals, so the prose lists below carry the whole model. The entity count and the state count would
both clear the diagram trigger in a session that can show one.

### 1a. Entities and relationships

- **Parcel** — one shipment, identified by a tracking number. Belongs to one Recipient, addressed by
  one Carrier, occupies at most one Compartment.
- **Compartment** — one lockable box. Belongs to one Bank (inferred). Holds zero or one Parcel.
- **Pickup code** — six digits, tied to one Parcel and one Compartment.
- **Bank** *(inferred)* — a set of Compartments at one site. Section 11 reports "per bank" and
  Section 12 gives it a network link, so it is load-bearing, and Section 3 does not list it.
- **Event log** *(inferred)* — belongs to one Bank; holds one entry per deposit and per opening
  (Section 9).
- **Recipient** — named as an actor, and carries no entity record. The phone number the SMS path
  depends on appears in no entity.
- **Carrier** *(inferred)* — sends the manifest that creates a Registered parcel, and receives an
  expired parcel back. Not in the actor list.
- **Manifest** *(inferred)* — the carrier's notice that creates the Registered state.

### 1b. States and transitions

States of Parcel:

1. **Registered** — entered when the carrier's manifest arrives; exits to Stored (courier deposit).
   No other exit is stated.
2. **Stored** — entered at deposit; exits to PickedUp (recipient closes the door) or to Expired (the
   03:00 sweep, once the window has run out).
3. **PickedUp** — entered when the door closes on a pickup. Terminal, and stated as terminal.
4. **Expired** — entered by the sweep. "An expired parcel is returned to the carrier" names an
   outcome and no state. **No exit** — see F12.

States of Compartment:

1. **free** — exits to occupied at deposit.
2. **occupied** — exits to free when the door closes on a pickup.

The document names no state for a compartment that has been opened for a deposit that has not
happened yet, and none for one holding an expired parcel awaiting return. See F3.

### 1c. Actor–action assignments

- Register a parcel — the carrier's manifest arrives; the carrier is not in the actor list.
- Scan badge, scan tracking number, place parcel, shut door — Courier.
- Open a free compartment at deposit — "the locker bank" (automated).
- Mark Stored, generate the pickup code, send the SMS — "Cedarline" (component not named).
- Deliver the SMS, report delivery asynchronously — Notification service (third party).
- Retry a failed send three times — Cedarline (implied by Section 10's wording).
- Enter the code, take the parcel, close the door — Recipient.
- Open the compartment on a valid code — "the bank" (automated).
- Run the expiry sweep at 03:00 — **initiator not stated**; the sweep has no owner and no location.
- Return an expired parcel to the carrier — **initiator not stated**.
- Open any compartment with a service badge — Operator.
- Read the dashboard — **initiator not stated**; no role is named for Section 11.

### 1d. Composition and boundaries

Four components are implied and none is declared: the locker bank (local, holds the keypad, the
doors, and the event log, and works while its link is down), the Cedarline central side (holds the
manifest, the parcel state, and the code generator), the SMS gateway (third party, asynchronous), and
the carrier's system (sends manifests, receives returns). The document never says which side of the
bank/central boundary validates a code, runs the 72-hour timer, or executes the sweep. See F2.

### What I assumed

- I read "Cedarline" in Section 5 as the central side rather than the locker bank, because Section 5
  contrasts it with "the locker bank" one sentence earlier. If Cedarline there means the bank itself,
  F2 and F20 change shape and F20 may dissolve.
- I read the expiry sweep as central and once-global rather than per-bank, because Section 7 gives one
  time and no per-bank qualification. If each bank sweeps itself, F25 stays and F19's second instance
  changes.
- I read "the pickup window is 72 hours from deposit" as measured from the physical door-shut, since
  that is what "deposit" names in Section 5. F7 exists because the document supports at least three
  other readings.
- I treated the pricing, the carrier contract, the physical hardware design, and the mobile or web
  channel a recipient might use as out of scope, since the document mentions none of them.
- I inferred Bank, Event log, Carrier, and Manifest as entities; none is in Section 3.
- I found no authoritative surface for parcel records named in this doc. If one exists in the product
  — a carrier tracking system that owns the parcel's public status — this deposit operation does not
  register with it.
- I found no authoritative surface for compartment inventory named in this doc. If one exists, the
  operator servicing path in Section 8 does not register with it.
- The interpretation rule: nowhere does the author state a craft standard out loud, so this review
  applied none on their behalf. Where I sharpened something, it is marked in the finding.

---

## Phase 2 — Structural issues in the model

F1 — The carrier acts twice in this flow and is not an actor

> "**Registered** — the carrier has told Cedarline the parcel is coming." — Section 4. Parcel states

Section 2 lists four actors and the carrier is not among them, yet the carrier creates the first
state and receives the parcel back at the end ("An expired parcel is returned to the carrier",
Section 7). Neither transition has an owner. Nobody knows who acts when a manifest arrives twice for
one tracking number, and nobody knows who physically carries an expired parcel out of the
compartment — the operator is the only person on site and Section 8 gives them a service badge and no
duty. The consequence is an expired parcel that stays in the compartment because the return is
nobody's job, which is the capacity failure Section 13's own TBD is about.

Add the Carrier to Section 2 with the two actions it owns: sending the manifest, and accepting a
return. Then write the return as a transition with a named actor and a time bound — either (a) the
operator removes expired parcels on the next service round, simple and slow; or (b) the sweep raises
a per-bank collection task the operator's device shows, which needs a task surface this document does
not have. I prefer (a) for release 2, with a stated maximum time in the compartment.

`defect · unclear-owner (actors)`

F2 — "Cedarline" and "the bank" act interchangeably, and the boundary between them is never drawn

> "the locker bank opens a free compartment... Cedarline then marks the parcel Stored, generates a
> pickup code, and sends the code to the recipient by SMS." — Section 5. Deposit

Two components appear in one sentence and the document never says which one holds what. It matters
at every step: Section 6 says "The bank opens the compartment" on a code entry without saying whether
the bank checks the code locally or asks Cedarline, and Section 12 says the bank works with its link
down. A recipient at an offline bank either gets their door opened or does not, and this document
supports both readings. The observable outcome is a support call the operator cannot answer, because
nobody can say from the spec whether the failure is expected.

Add a short composition section naming the two sides and what each one owns: parcel state, code
generation, code validation, the timer, the sweep, and the event log, one owner per row. State the
protocol between them in one sentence per direction. That table is the artifact F20 and F23 both
depend on.

`defect · boundary-issue (composition)`

F3 — Compartment has two states and the flow needs at least four

> "A compartment is free or occupied." — Section 3. Entities

Between "the locker bank opens a free compartment" and "the courier... shuts the door" the
compartment is open and empty, and it is neither free nor occupied under any reading that is safe. A
second missing state sits at the other end: a compartment holding an expired parcel is occupied and
must not be offered to the next courier, and the document gives the bank no way to tell the two
apart. A courier at a bank with one apparently-free compartment is handed a door that another courier
is standing at, or one with an expired parcel inside, and two parcels end up in one box — which
breaks the stated rule in Section 9.

Give Compartment four states: `free`, `reserved` (opened for a deposit, no parcel yet), `occupied`,
and `awaiting-return` (holds an expired parcel). Write the transition out of `reserved` on both
outcomes, and state that only `free` compartments are offered at deposit.

`defect · missing-scenario (state-space)`

F4 — Bank is not an entity, and its link state is a hidden parameter that changes behaviour

> "A bank works while its network link is down, and it syncs events when the link returns." —
> Section 12. Non-functional

Section 3 lists three entities and Bank is not one, while Section 11 reports per bank and Section 12
gives a bank a network link with two states. That link state changes what deposit, pickup, and the
sweep can do, and no flow in Sections 5 to 7 names which mode it is describing. An operator reading
the dashboard cannot tell a bank with no free compartments from a bank that has not reported in a
day, because the model has no place to hold the difference.

Add Bank to Section 3 with its compartments, its site, and a `link` field reading `online` or
`offline` with the timestamp of the last successful sync. Then write each of Sections 5, 6, and 7
against both link values — the online row is what is written today.

`defect · missing-scenario (state-space)`

F5 — The pickup code has no lifecycle and no uniqueness rule

> "**Pickup code** — a six-digit code tied to one parcel and one compartment." — Section 3. Entities

The code is an entity with no states, though Section 10 gives it at least four: generated, sent,
delivery reported, and failed after three retries. Nothing says two active codes in one bank must
differ. A bank with fifty compartments drawing six-digit codes at random will eventually hold two
parcels with the same code, and Section 6's "The bank opens the compartment holding that parcel" then
names no compartment — the bank picks one, and a recipient walks off with a stranger's parcel while
their own is marked PickedUp by the door close.

Two artifacts. First, add the uniqueness invariant: no two parcels at one bank hold the same active
code, and generation retries on a collision. Second, give the code the states Section 10 already
implies, so the dashboard in F27 has something to show. If the code space is meant to be per-bank
rather than global, say which — I read it as per-bank because the keypad is per-bank.

`defect · missing-rule (invariant)`

---

## Phase 3 — Property analysis

### 3a. Safety — things that must never happen

F6 — Deposit is one sentence covering four steps with no failure behaviour between them

> "Cedarline then marks the parcel Stored, generates a pickup code, and sends the code to the
> recipient by SMS." — Section 5. Deposit

The courier has already shut the door, so the physical act is irreversible while three system steps
remain. Where code generation fails after the state flip, the parcel is Stored with a running 72-hour
window and no code exists. The recipient receives nothing, and the nightly sweep expires a parcel
that was never collectable. The courier sees a completed deposit and walks away.

Make the pickup code's existence a precondition of the Stored state. Generate the code before the
door-shut event flips state, and write that a parcel with no code stays out of Stored and starts no
window. Add the compensating action for a generation failure — an operator alert naming the bank and
the compartment.

(This finding matches the worked example printed in `SKILL.md`. I reached it from the document and
kept it, because it is real; it is listed here so a reader knows it is not an independent second
sighting.)

`defect · partial-success-risk (atomicity)`

F7 — The 72-hour window's start instant is never fixed

> "The pickup window is 72 hours from deposit." — Section 6. Pickup

"Deposit" names four candidate instants in Section 5: the tracking scan, the door shut, the Stored
flip, and the SMS send. They can be minutes apart, and under Section 10's retry ladder the send can
be fifteen minutes behind the door. A recipient who collects at hour 71:50 is inside the window on one
reading and outside it on another, and the sweep and the keypad may be reading different clocks —
Section 12 puts the keypad on a bank that runs while its link is down. The observable outcome is a
compartment that refuses a code the recipient believes is live, with no error the operator can trace.

Fix the start at one named event and write it into Section 6: "the window starts at the door-shut
event that completes the deposit." State which clock stamps it, the bank's or Cedarline's, since F2
leaves that open too.

`defect · missing-rule (invariant)`

F8 — Closing the door marks the parcel PickedUp with no check that the parcel left

> "Closing the door marks the parcel PickedUp and the compartment free." — Section 6. Pickup

A recipient who opens the compartment, looks at a parcel that is not theirs or changes their mind,
and shuts the door has just marked the parcel PickedUp and the compartment free. The parcel is
physically inside. The next courier is offered that compartment as free and puts a second parcel in
it, which breaks the stated rule that a compartment holds one parcel at a time. Two recipients then
hold codes for one box, and the dashboard shows a stored count that is one short.

Add the postcondition to Section 6 and name what observes it: either (a) a weight or door sensor
reading empty before the state flips, which needs hardware this document has not claimed; or (b) the
state flip stays, and the operator servicing round in Section 8 gets a stated duty to reconcile a
compartment found non-empty against the parcel record. I prefer (a) if the hardware exists, since (b)
leaves a window in which the bank offers an occupied box.

`defect · missing-outcome-check (postcondition)`

F9 — Deposit has no precondition on the parcel's current state

> "A parcel whose tracking number is unknown to Cedarline is refused at the scan, and the bank opens
> no compartment." — Section 5. Deposit

The only stated precondition is that the number is known. A number that is already Stored at another
bank is known, and so is one that is PickedUp or Expired. A courier scanning a returned parcel's old
number, or scanning the same number twice at two banks, gets a compartment opened both times. One
parcel record then claims two compartments, its single pickup code opens one of them, and the second
compartment is occupied by a parcel the system believes is elsewhere — invisible until an operator
finds it.

Write the precondition into Section 5: a deposit is accepted only for a parcel in Registered.
Name the refusal for each other state, and give the courier the reason, which F31 also asks for.

`defect · missing-prerequisite (precondition)`

F10 — The courier badge is scanned and nothing says what the scan checks

> "The courier scans their badge" — Section 5. Deposit

The badge appears in Section 2 and in Section 5 as a step, and no rule says an unknown, expired, or
revoked badge refuses the deposit — Section 5's only refusal is on the tracking number. Read as
written, anyone holding any badge and a valid tracking number opens a compartment at any bank. The
observable outcome after a badge is lost is a deposit trail with a courier identity nobody can trust,
which is the identity the event log in Section 9 is recording.

Write the badge check as a precondition with its three refusals: unknown badge, revoked badge, and a
badge not authorized for that bank if authorization is per-bank. State which of the three the
document intends — I read the badge as a global courier credential, and if it is per-carrier, say so.

`defect · missing-prerequisite (precondition)`

F11 — Nothing recovers a compartment the courier opened and walked away from

> "The courier puts the parcel in and shuts the door." — Section 5. Deposit

The document writes this as one step and gives no behaviour for its failure: a courier who is called
away, drops the parcel, or finds the compartment too small leaves an open, empty door. Nothing closes
it, nothing frees it, and no state exists for it (F3). The parcel record is either Registered with an
open box against it or already Stored under F6's ordering. The next person at the bank sees an open
compartment, and the operator learns about it when a customer reports it.

Add a stated timeout on the reserved compartment — an auto-close with the deposit abandoned and the
parcel left Registered — and write the log line the bank emits when it fires. Name the timeout's
length, or mark it as a provisional default so the count in Phase 5 sees it.

`defect · unclear-recovery (rollback)`

### 3b. Liveness — things that must eventually happen

F12 — Expired is a dead end: no state, no actor, no time bound

> "The expiry sweep runs daily at 03:00 and moves every parcel whose pickup window has run out into
> Expired. An expired parcel is returned to the carrier." — Section 7. Expiry

Section 4 marks PickedUp terminal and says nothing about Expired, and the return is an outcome with
no transition behind it. The parcel stays in the compartment with no state saying it is on its way
out and no time by which it must be gone. Compartments are the scarce resource in this product: every
unreturned expired parcel is one fewer box at that bank forever, and the courier who arrives at a
full bank has no procedure — that is Section 13's own TBD, reached from a different direction.

Add a `Returned` state to Section 4, entered when the parcel physically leaves the compartment, and
write the transition with the actor F1 asks for and a stated maximum time in the compartment after
expiry. The dashboard in Section 11 then gets a fourth counter, parcels awaiting return, which is the
number that predicts a full bank.

`defect · no-exit (dead-end)`

F13 — Registered has no exit but deposit, and a stale manifest stays depositable forever

> "**Registered** — the carrier has told Cedarline the parcel is coming." — Section 4. Parcel states

Nothing cancels a Registered parcel and nothing ages one out. A parcel the carrier re-routed, lost,
or delivered to the door stays Registered indefinitely, and Section 5's only scan check is that the
number is known — so months later that number still opens a compartment at any bank. The observable
outcome is a Registered backlog nobody can distinguish from the parcels actually in transit, and a
deposit against a tracking number the carrier has closed on their side.

Add two exits to Registered: a carrier cancellation, with the carrier as its actor (F1), and an
expiry of the registration itself after a stated number of days. State the number, or mark it as a
provisional default.

`defect · stuck-state (liveness)`

F14 — After the third SMS retry fails, nothing happens

> "Cedarline retries a failed send three times, at one minute, five minutes, and fifteen minutes." —
> Section 10. Notification

The ladder ends and the document stops. The parcel is Stored, its window is running, and the
recipient has no code and no reason to expect one. Seventy-two hours later the sweep expires a parcel
the recipient was never able to collect, and the first person who learns of it is the recipient
chasing the carrier. Nothing in Sections 10 or 11 shows an operator the difference between this
parcel and any other stored one.

Write the terminal branch: after the third failure the parcel is flagged undeliverable-code, an
operator alert names the bank, the compartment and the recipient, and the pickup window pauses or
restarts on a successful resend. State which of pause or restart applies — I prefer a restart from
the first successful send, since it is the instant the recipient could first act.

`defect · stuck-state (liveness)`

### 3c. Whether the spec can be enforced

F15 — The one-minute code guarantee cannot be discharged, and Section 10 contradicts it directly

> "Every parcel receives its pickup code within one minute of deposit." — Section 9. Stated rules

Three things break this. The retry ladder in Section 10 places its second attempt at five minutes and
its third at fifteen, so the document's own failure path exceeds the guarantee by design. Delivery is
a third party's act — "The gateway accepts a send request and reports delivery asynchronously" — and
Cedarline can promise a send, not a receipt. And "receives" names an event Cedarline observes only
through an asynchronous report, so nobody can measure compliance. An operator asked whether the rule
held yesterday has no number to answer with.

Split the rule into the part Cedarline owns and the part it does not: "Cedarline submits the pickup
code to the gateway within one minute of the door-shut event", plus a separate stated target for
delivery with the gateway's own contract behind it. Name where the one minute is measured, which is
the same measurement point F30 asks for across all budgets.

`defect · unenforceable-promise (discharge)`

F16 — "Only the recipient can open a compartment" cannot be discharged by a six-digit code

> "Only the recipient can open a compartment holding a parcel." — Section 6. Pickup

The code is a bearer token: whoever types it opens the door, and the bank cannot tell the recipient
from anyone else. No attempt limit is stated anywhere, and Section 12 puts keypad-to-open under two
seconds, so a person standing at a bank can try codes continuously. Against fifty active codes in a
six-digit space, a patient attacker opens a stranger's compartment within hours, and the event log
records a legitimate-looking opening. Section 13's own open question about handing a code to someone
else is the same rule seen from the friendly side.

Weaken the claim to what the mechanism delivers — "a compartment holding a parcel opens only to that
parcel's pickup code" — and add the enforcement the strong claim needs: an attempt limit per keypad
per interval with a stated lockout, and a stated code lifetime. If Cedarline wants the strong claim
literally, it needs a second factor at the keypad, which is a release 3 decision, not a wording fix.

`defect · unenforceable-promise (discharge)`

### 3d. Internal consistency

F17 — Section 6 and Section 8 openly conflict on who can open a compartment

> "Only the recipient can open a compartment holding a parcel." — Section 6. Pickup
> "An operator with a service badge can open any compartment in a bank" — Section 8. Operator servicing

Both are stated as rules and they cannot both hold. Beyond the wording, the operator path has no
consequences written at all: opening a compartment holding a Stored parcel changes no state, revokes
no code, writes nothing the recipient can see, and stops no window. An operator who takes a parcel out
during a cleaning round leaves a Stored parcel that is not there; the recipient arrives, the door
opens on an empty box, the door closes, and the parcel is PickedUp.

Rewrite the Section 6 rule as "a compartment holding a parcel opens to that parcel's pickup code or
to a service badge", and add to Section 8 what an operator open does to parcel state: which of the
three service reasons removes the parcel, what state a removed parcel takes, and what the recipient is
told. The three reasons Section 8 lists — a jammed door, a parcel left by mistake, a cleaning round —
need different answers, and the document currently gives them one.

`defect · direct-contradiction (contradiction)`

F18 — The window is stated as 72 hours and the sweep that ends it runs once a day

> "The pickup window is 72 hours from deposit." — Section 6. Pickup
> "The expiry sweep runs daily at 03:00" — Section 7. Expiry

Nothing acts at the 72-hour mark: the code keeps working until the next sweep. A parcel deposited at
03:01 is swept at 03:00 three days later, one minute short, and waits another day — 95 hours 59
minutes. A parcel deposited at 02:59 gets 72 hours and one minute. The real window is a range from 72
to 96 hours depending on the minute of deposit, and the recipient was told 72. A carrier promised a
return after 72 hours waits up to an extra day, and two recipients depositing an hour apart get
visibly different treatment at the same bank.

Pick one and write it: (a) the code stops working at exactly 72 hours and the sweep only moves state,
which keeps the promise and needs the revocation F19 also asks for; or (b) the window is stated as
"until the first sweep after 72 hours", and the recipient's SMS carries the actual deadline
timestamp. I prefer (a) — (b) tells the truth but hands the recipient a variable deadline.

`defect · direct-contradiction (contradiction)`

F19 — A code stops working when the parcel leaves, so an expired parcel is still collectable

> "A pickup code opens one compartment and stops working once the parcel leaves it." — Section 9.
> Stated rules

Expiry moves state and moves nothing physical, so the parcel has not left the compartment and the
code has not stopped by this rule. Two instances of the same gap:

- **at the sweep** — a recipient arriving at hour 80 types their code, the door opens, they take the
  parcel. The record says Expired, the carrier has been told to expect a return that will never
  arrive, and the door close either fires a Stored-to-PickedUp transition from the wrong state or
  fires nothing;
- **at an offline bank** — Section 12 lets a bank run with its link down, so even a central
  revocation at exactly 72 hours (F18's option a) does not reach the keypad. The bank opens on a code
  Cedarline has already killed, and learns of it at the next sync.

Write revocation as an explicit act with a named owner: expiry revokes the code at the bank, and the
bank refuses a revoked code locally from its own clock. State what the bank does with a code whose
status it cannot confirm while offline — refuse or allow — because that is the decision the offline
mode turns on.

`defect · internal-conflict (consistency)`

F20 — Offline operation and the deposit flow cannot both hold as written

> "A bank works while its network link is down, and it syncs events when the link returns." —
> Section 12. Non-functional

Deposit needs the central side three times: the tracking number is checked against what "Cedarline"
knows, Cedarline marks the parcel Stored, and Cedarline generates and sends the code. An offline bank
can do none of them. Read as written, a courier at an offline bank either has every deposit refused —
which is not "works" — or deposits into a compartment with no record and no code, and the recipient
gets nothing until the link returns, with the 72-hour window either already running or not yet
started, which the document also does not say.

State what "works" covers per flow. My reading is that pickup and operator servicing work offline and
deposit does not, and if that is the intent, write it: "an offline bank accepts no deposits and
refuses at the badge scan with a stated message." If deposits must work offline, the bank needs local
code generation and a reserved code range, which is a design decision, not a sentence.

`defect · internal-conflict (consistency)`

F21 — The dashboard's counts and the occupancy rule are two homes for one fact with nothing tying them

> "The operations dashboard shows, per bank: compartments free, parcels stored, and parcels expired
> today." — Section 11. Reporting

Compartments free and parcels stored are derivable from each other through Section 9's "A compartment
holds one parcel at a time", and no sentence states the tie. They drift the moment any of F8, F11, or
F17 happens: a compartment freed with a parcel still inside, a reserved box nobody closed, an
operator removal that changes nothing. An operator watching a bank fill up sees two numbers that no
longer add up and has no rule saying which one is wrong, so the reconciliation is a judgment call made
per incident.

Add the invariant as a sentence: at any instant, compartments occupied at a bank equals parcels at
that bank in Stored plus parcels awaiting return. Then name what watches it — a nightly reconciliation
that raises the mismatch as an operator task is the cheap version, and the alternative is the
dashboard deriving one number from the other and never storing both.

`defect · missing-rule (invariant)`

### 3e. Generative stress-testing

`reference/stress-lenses.md` was read in full before these findings were written. Sweep verdicts are
in the table at the end of this phase; imaginative probes owe none, and the two they produced are
named in their findings.

F22 — The declared rules name no enforcer, and the log rule covers three surfaces it does not reach

> "Every deposit and every opening is written to the bank's event log." — Section 9. Stated rules

Section 9 is this document's declared-laws section: four laws that hold across every surface. None
names the thing that fails when it is broken — no test, no gate, no named reviewer, no operator
report. The log law is the sharpest case, because its clause is missing on the surfaces where it
matters most: the expiry sweep writes nothing, the code generation and SMS send write nothing, and it
is not stated whether an operator's service open counts as "an opening". An investigator asked why a
parcel was expired and returned has a log with the deposit and the openings and no record of the
decision that expired it.

Two artifacts. First, add a column to Section 9 naming each law's enforcer, using the three that
qualify: a mechanical gate, this review where the violation pins to a sentence, or a
design-consistency review's soft recommendation. Second, list the events the log holds, one row per
surface — deposit, recipient open, operator open, code generated, code sent, send failed, expiry
decision — and name the retention period. Note that with no test suite verified for this project,
this review is currently the only reader of these laws.

`defect · missing-rule (invariant)`

F23 — One dependency's failure is described and three are silent

> "A bank works while its network link is down, and it syncs events when the link returns." —
> Section 12. Non-functional

The bank's link is the one failure the document names, and the guarantee is scoped to it. The
remaining parts of the same domain are unanswered: the SMS gateway being down or slow past its
retries (Section 10 covers a failed send and not an unreachable gateway), the Cedarline central side
being down while banks are up, and a bank losing power mid-window and restarting — whether it comes
back holding its codes, its event log, and its door states. Each one is a live outage in which an
operator is asked what is happening and the document has no sentence for them.

Write one row per dependency: the gateway, the central side, the carrier's manifest feed, and bank
power. Each row names what still works, what is refused, and what the operator sees. A dependency
deliberately left out of release 2 gets a decided sentence saying so rather than silence.

`defect · missing-scenario (state-space)`

F24 — Retry and failure policy is written for one integration and none of its siblings

> "Cedarline retries a failed send three times, at one minute, five minutes, and fifteen minutes." —
> Section 10. Notification

Retry policy is a kind-general rule homed in one member's section. Three sibling integrations carry
none: the carrier manifest arriving (Section 4), the event-log sync when the link returns (Section
12), and the door-open command at the keypad (Section 6). The log sync is the one with an invariant
behind it — Section 9 promises every deposit and opening is logged, and a sync that fails once with no
retry silently breaks that promise, leaving an investigator a log with holes nobody flagged. This
review keeps no surface registry to enumerate against — the project has none — so this sweep read the
kind out of the sentence itself.

Lift the retry policy to a clause naming the integration class and listing its members, with each
member's attempts, intervals, and terminal branch. Where a member deliberately does not retry, say so
in its row.

`defect · missing-scenario (state-space)`

F25 — The 03:00 sweep can fire on a parcel a recipient is collecting

> "The expiry sweep runs daily at 03:00 and moves every parcel whose pickup window has run out into
> Expired." — Section 7. Expiry

Nothing states what the sweep does with a parcel whose compartment is open at that instant. A
recipient standing at a bank at 03:00:01 with the door open has their parcel moved to Expired
underneath them; they take it, the door closes, and Section 6's transition fires from a state Section
4 does not allow it from. The record then reads Expired, the carrier is told a return is coming, and
the parcel is in the recipient's hands. The mirror case is a deposit landing at 02:59:59 against a
sweep that reads the parcel list a second later.

State the sweep's precondition: it skips any parcel whose compartment is currently open or whose
pickup is in progress, and it re-reads them on the next run. Name the two-writer rule in one sentence
— the keypad transaction holds the parcel while the door is open — since F17's operator path needs
the same rule.

`defect · undefined-path (transitions)`

F26 — The dashboard reports per-bank numbers with no answer for a bank that is offline

> "The operations dashboard shows, per bank: compartments free, parcels stored, and parcels expired
> today." — Section 11. Reporting

Section 12 lets a bank run disconnected and sync later, so the dashboard's per-bank row is as old as
that bank's last sync and the document gives it no staleness mark. An operator choosing where to
drive sees a bank with three free compartments that filled up yesterday, and a bank that reported
nothing for two days is indistinguishable from a quiet one. The dispatch decision is made on numbers
nobody can date.

Add the last-sync timestamp per bank row and a stated staleness threshold past which the row reads as
unknown rather than as a number. Name the threshold, or mark it as a provisional default.

`defect · hard-to-monitor (observability)`

F27 — SMS delivery is asynchronous and no surface shows pending, arrived, or failed

> "The gateway accepts a send request and reports delivery asynchronously." — Section 10.
> Notification

The delivery report arrives into a place the document never names. The dashboard shows three counters
and none of them is about codes, so a parcel whose code is in flight, delivered, or dead after three
retries looks the same as any stored parcel. An operator taking a call from a recipient who never got
a code cannot say whether the code was sent, whether the gateway accepted it, or whether it failed
three times overnight — and the answer decides whether they resend or drive out to the bank.

Add a per-parcel code delivery status with the three states the async path already has — pending,
delivered, failed — and put the failed count on the dashboard beside the three existing counters.
That counter is what makes F14's terminal branch visible to somebody.

`defect · hard-to-monitor (observability)`

### Coverage tables

CRUD coverage per entity:

| Entity | Create | Read | Update | Delete | Notes |
|---|---|---|---|---|---|
| Parcel | covered — manifest arrival (§4) | partial — dashboard counts only, no per-parcel read stated | partial — state changes stated, no correction path (F17) | missing — no removal, no retention stated | Registered has no cancel (F13) |
| Compartment | missing — banks and their boxes are provisioned by nobody | covered — dashboard free count (§11) | partial — free/occupied only (F3) | missing | out-of-service compartment has no state (F17 jam case) |
| Pickup code | covered — generated at deposit (§5) | partial — the recipient reads it by SMS; no operator read (F27) | missing — no reissue path (F14) | partial — "stops working once the parcel leaves" (F19) | no uniqueness rule (F5) |
| Bank | missing — not an entity (F4) | covered — per-bank dashboard row (§11) | missing | missing | link state unmodelled (F4) |
| Event log entry | covered — deposits and openings (§9) | missing — no reader, no query, no retention stated | N/A — append-only by nature | missing — no retention (F22) | three surfaces write nothing (F22) |

Invariants per state:

| State | Invariants stated | Invariants missing |
|---|---|---|
| Registered | none | tracking number is unique among live parcels; a registration ages out (F13) |
| Stored | a compartment holds one parcel at a time (§9); the window is 72h (§6) | a Stored parcel has exactly one active code (F6); a Stored parcel occupies exactly one compartment (F9); the window's start instant (F7) |
| PickedUp | terminal (§4) | the compartment is physically empty (F8); the code is dead (F19) |
| Expired | none | the parcel is still in the compartment until returned (F12); the code is dead (F19); a maximum time before return (F12) |
| Compartment free | free or occupied (§3) | free implies no parcel inside (F8); free implies offerable at deposit (F3) |
| Compartment occupied | holds one parcel (§9) | occupied implies exactly one parcel record points at it (F9) |

Authorization per action:

| Action | Roles allowed | Granular check enforceable? | Notes |
|---|---|---|---|
| Deposit a parcel | Courier with a badge | no — nothing states what the badge check refuses (F10) | no per-bank or per-carrier scoping stated |
| Open a compartment at pickup | Recipient, by code | no — a six-digit bearer code with no attempt limit (F16) | contradicted by the operator path (F17) |
| Open any compartment | Operator with a service badge | partly — the badge is named, its check is not | no state consequences written (F17) |
| Run the expiry sweep | not stated | N/A | no initiator named (Phase 1c) |
| Read the dashboard | not stated | no — no role model exists in this document | per-bank scoping not stated |
| Register a parcel | Carrier | no — the carrier is not an actor (F1) | no authentication of the manifest feed stated |

Mandatory-sweep verdicts, one cell per sweep per surface:

| Surface | Cross-cutting laws | Edge conditions | Policy uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| Deposit at the locker bank (§5) | hit (F22) | hit (F11) | N/A — no surface registry | hit (F6, F7) | hit (F20) |
| Pickup keypad (§6) | hit (F22) | hit (F18, F19) | hit (F17 — kind-general rule homed on one member) | hit (F8) | hit (F25) |
| Expiry sweep (§7) | hit (F22) | hit (F18) | N/A — no surface registry | hit (F12) | hit (F25) |
| Operator servicing (§8) | hit (F22) | clean | hit (F17) | hit (F17 — one-sided pair: open with no stated close) | hit (F17) |
| Notification send (§10) | hit (F15) | hit (F14, F27 — async pending/arrived/failed) | hit (F24) | hit (F5) | hit (F23) |
| Operations dashboard (§11) | clean | clean | N/A — no surface registry | clean | hit (F26) |
| Carrier manifest intake (§4) | hit (F22 — no log clause) | clean | hit (F24) | hit (F13) | hit (F23) |

Class lens: swept — the expiry-revocation class (F19) and the dependency-failure class (F23).

Notes on the table. The policy-uniformity sweep's registry-based enumeration is N/A throughout — this
project keeps no surface registry — so where that sweep reads "hit" it fired on the kind-general-rule
read, which needs no registry. Where it reads N/A, the registry read was the only one available for
that surface. The surface list itself was derived by this reviewer from the document's sections, and
it is not an authority; a registry the project later keeps may divide these differently.

The probes owe no verdict, and the class lens beside them owes the line under the verdict table.
Two imaginative probes produced findings and are named where they landed: ambiguity and ties (F5),
concurrency and order (F25). Two produced the assumption lines in "What I assumed" rather than
findings, per the surface-authority lens's own rule: no authoritative surface for parcel records or
compartment inventory is named in this document. The class lens fired twice, and both findings list
their instances rather than a single spot: F19 (expiry revocation, at the sweep and at an offline
bank) and F23 (four dependencies). Delivery separability along a declared axis: no cross-cutting
composition axis is declared in this document, so it stays silent. False serialization: this is not a
concurrency plan, so it stays silent too.

---

## Phase 3.5 — Acknowledged gaps

Three items in Section 13. They carry A-numbers rather than F-numbers, since the pass files no new
finding for a gap the document already flags.

A1 — No procedure exists for a courier at a full bank

> "**TBD:** what the courier does when a bank has no free compartment at deposit time." — Section 13.
> Open items

The second-order consequence is that this TBD is not an edge case in this design, it is the expected
steady state. Nothing returns an expired parcel (F12), nothing recovers an abandoned reserved
compartment (F11), and nothing frees a compartment whose parcel was taken by an operator (F17). Each
one is a compartment permanently gone, so banks fill up on a one-way ratchet, and this TBD becomes the
daily case rather than the rare one.

Two options. (a) The courier is refused at the tracking scan with a stated message and the parcel goes
back on the van — simple, and it pushes the failure onto the carrier's redelivery process. (b) The
bank holds an overflow queue and the courier is directed to another bank the app names — better for
the recipient, and it needs a bank-to-bank routing surface this document does not have. I prefer (a)
for release 2, on the condition that F12 and F11 are fixed first, since without them (a) is a slowly
closing door.

`acknowledged · missing-scenario (state-space)`

A2 — Whether a recipient may hand their code to someone else

> "**Open question:** should a recipient be able to hand their code to someone else, and does the spec
> need to say anything about it?" — Section 13. Open items

The document has already answered this by accident, in two places that disagree. Section 6 says only
the recipient can open a compartment, which forbids it; the mechanism is a bearer code, which permits
it and cannot tell the difference (F16). So the open question is not whether to allow it — it is
allowed today — but whether the written rule keeps claiming otherwise. The operational cost of leaving
it open lands on a support agent taking a call from a recipient whose neighbour collected the parcel,
with no rule to read out.

Two options. (a) Bless it: the code is a bearer token, anyone holding it may collect, and the SMS says
so. (b) Bind it: the keypad asks for a second factor tied to the recipient, and handing the code on
stops working. I prefer (a) for release 2 — it matches the mechanism, it needs a wording change and
no hardware, and it lets F16's claim be rewritten honestly.

`acknowledged · unenforceable-promise (discharge)`

A3 — Damage refunds are out of scope, and the damaged parcel's state is not

> "The refund path for a parcel damaged inside a compartment is out of scope for release 2." —
> Section 13. Open items

This one is a decided scope exclusion rather than a TBD, and it is worth a note because the exclusion
covers the money and not the parcel. Section 8 already names "a parcel left by mistake" as a
serviceable case, and neither it nor a damaged parcel has a state to move to (F17). An operator
holding a crushed parcel has no transition, so the record stays Stored, the recipient's code keeps
working on an empty box, and the sweep eventually reports a return that never happened.

Keep the refund out of release 2, and add the state anyway: a `Removed` state with the operator's
reason recorded — jammed, damaged, misplaced, or cleaning. The refund path in release 3 then has
something to attach to.

`acknowledged · missing-scenario (state-space)`

---

## Phase 4 — Human and operational factors

F28 — The document never says what the SMS carries beyond the code

> "sends the code to the recipient by SMS" — Section 5. Deposit

The code is the only content specified. A recipient receiving six digits does not learn which bank
holds the parcel, which supermarket or transport hub that is, when the window closes, or who sent it —
and a recipient with two parcels in flight cannot tell the messages apart. The observable outcome is
a recipient who drives to the wrong bank, or who does not go at all because the message reads like a
scam, and a parcel that expires with a delivered code against it. This is also the message where the
deadline from F18 has to appear if option (b) there is chosen.

Write the message contract in Section 10: the fields the SMS carries — bank name and address,
compartment number if it is shown, the deadline as a local timestamp, the parcel's carrier reference,
and the code — with the sender identity the recipient sees. Add the same list for a resend after F14's
terminal branch.

`defect · missing-outcome-check (postcondition)`

F29 — The keypad's answer to a wrong, expired, or unknown code is unstated

> "The recipient types the six-digit code on the bank's keypad. The bank opens the compartment holding
> that parcel." — Section 6. Pickup

One path is written and the rest are blank. A recipient typing a mistyped code, an expired code, a
code for a parcel at another bank, or a code that was revoked gets no stated response — no message, no
distinction between them, and no next step. The person then retypes it repeatedly, which is also the
behaviour F16's missing attempt limit has to tell apart from an attacker. Support receives "the locker
says nothing", which is not a report anyone can act on.

Write one row per failed entry — unknown code, expired window, wrong bank, revoked, too many attempts
— with the message shown, whether it names the reason, and what the recipient is told to do next.
Keep the messages in the recipient's vocabulary: a parcel, a locker, a deadline. The state names
Stored, PickedUp and Expired are Cedarline's internal words and stay off the keypad.

`defect · undefined-path (transitions)`

F30 — The two budgets name no measurement point and no watcher, and no scale ceiling is stated

> "Keypad entry to door open takes under two seconds." — Section 12. Non-functional

Two numbers appear in this document — under two seconds here, within one minute in Section 9 — and
neither says where it is measured or what fails when it is missed. Keypad-to-open spans the keypad,
the bank, possibly the network to Cedarline (F2), and a physical latch; measured at different points
the same event is well inside or well outside two seconds. No ceiling is stated anywhere for how big
this gets: compartments per bank, banks per dashboard, parcels per sweep run, or SMS sends per minute
at a peak. The nightly sweep is the one to watch, since it is a single global job over every parcel.

For each budget, add the measurement point and the watcher: the two-second one measured at the keypad
from the last keypress to the latch release, watched by a bank self-test that reports slow opens; the
one-minute one per F15. Then state the assumed ceiling — compartments per bank, banks in the fleet,
parcels swept per run — as the scale this design is claimed to hold at.

`recommendation · now · hard-to-monitor (observability)`

F31 — A refused courier is told nothing, and no security or privacy line exists anywhere

> "A parcel whose tracking number is unknown to Cedarline is refused at the scan, and the bank opens
> no compartment." — Section 5. Deposit

Two operational blind spots meet here. The refusal has no message and no reason, so a courier holding
a legitimate parcel whose manifest has not synced yet cannot tell that from a wrong parcel, and the
parcel goes back on the van with no record of the attempt. Separately, the recipient's phone number is
the pivot of the whole notification path and appears in no entity in Section 3 — nothing says where it
comes from, that a parcel without one cannot be deposited, how long it is kept, or who can read it
beside the gateway. Section 13 names three out-of-scope items and privacy is not among them, so this
reads as an omission rather than a decision.

Two artifacts. Give the scan refusal a reason code and a courier-facing message per case — unknown
number, already deposited (F9), wrong bank — and log the refused attempt. And add the recipient's
contact details to Section 3 as a field of the parcel, with a precondition that a parcel with no
usable number is refused at the scan, plus one stated line on retention and on who may read it. If
privacy genuinely sits with the carrier rather than with Cedarline, write that as the explicit skip.

`defect · missing-prerequisite (precondition)`

F32 — The deposit paragraph packs seven actions across three actors in three sentences

> "The courier scans their badge, scans the parcel's tracking number, and the locker bank opens a free
> compartment. The courier puts the parcel in and shuts the door. Cedarline then marks the parcel
> Stored, generates a pickup code, and sends the code to the recipient by SMS." — Section 5. Deposit

A reader tracking who acts at each step has to hold three actors and seven ordered actions in one
paragraph, and the ordering is load-bearing — F6 turns entirely on which step comes before the door
shut. This is a reading-load call rather than a rhetorical triad, because each item is a distinct
action with its own actor and its own failure mode. The author is the person who decides whether it
reads as a list, so this queues as a judgment call.

Rewrite Section 5 as a numbered list, one step per row, with the actor named on each and a column for
what happens when that step fails. That table is where F6, F9, F10, and F11 all land, so the rewrite
pays for itself.

`recommendation · later · confusing-for-users (cognitive-load)`

---

## Phase 5 — Closing summary

### 1. Top three to fix before development

1. **F20 and F2** — offline operation and the deposit flow contradict each other, and the
   bank-versus-central boundary that would settle it is never drawn. Everything else about degraded
   mode waits on this.
2. **F6, F7 and F8** — deposit and pickup each collapse several steps into one sentence, so an
   irreversible physical act sits beside unwritten failure behaviour and the window's start instant is
   undefined.
3. **F12 with F1** — Expired is a dead end with no actor and no time bound, which makes Section 13's
   own capacity TBD (A1) a certainty rather than an edge case.

### 2. Properties the document should state explicitly

Each of these is written to be pasted straight in.

- "A parcel enters Stored only when a pickup code exists for it, and the 72-hour window starts at the
  door-shut event that completes the deposit."
- "At any instant, the number of occupied compartments at a bank equals the number of parcels at that
  bank in Stored plus the number awaiting return."
- "No two parcels at one bank hold the same active pickup code."
- "A compartment holding a parcel opens to that parcel's active pickup code or to a valid service
  badge, and to nothing else."
- "A pickup code is dead from the moment the parcel's window ends, whether or not the parcel has left
  the compartment, and a bank refuses a dead code from its own clock while offline."
- "Every parcel that enters Expired leaves its compartment within N hours, and the parcel's state
  moves to Returned when it does."
- "A deposit is accepted only for a parcel in Registered."
- "Every deposit, every opening, every code generated or sent, and every expiry decision is written to
  the bank's event log, and the log is retained for N days."

### 3. Open questions needing the author

Only the ones inspection cannot settle:

1. Does "a bank works while its network link is down" mean deposits must work offline, or that pickup
   and servicing work while deposits are refused? (F20) The answer decides whether the bank needs local
   code generation, which is a hardware and security decision.
2. Is the pickup code meant as a bearer token or as a claim about the recipient's identity? (F16, A2)
   Business call, not a wording fix.
3. Who owns the physical return of an expired parcel, Cedarline's operator or the carrier's driver?
   (F1, F12) This is a contract question between two companies.
4. What is the assumed fleet scale — compartments per bank and banks in the fleet? (F30) Nothing in the
   document implies it.
5. Which of the three operator service reasons removes a parcel from a compartment, and what should the
   recipient be told when it happens? (F17)

### 4. Recommendations queued for a judgment call

- **F30** — `recommendation · now`. The two stated budgets get a measurement point and a watcher, and
  the document states its scale ceiling. Queued rather than blocking, since nothing stated is false.
- **F32** — `recommendation · later`. Section 5's deposit paragraph becomes a numbered step list with
  a failure column. Worth doing at the same time as F6, and worth nothing on its own.

### 5. Provisional defaults in the document

**Count: 0.** The document carries no `[default]` marks and no equivalent — no sentence states a
behaviour while marking itself unratified. Nothing to list, and nothing to age.

Two notes on that zero. The three items in Section 13 are acknowledged gaps, not provisional defaults:
they answer nothing, where a provisional default states a behaviour and marks it unconfirmed. And
several fixes proposed above deliberately create the document's first provisional defaults — the
reserved-compartment timeout (F11), the registration age-out (F13), and the dashboard staleness
threshold (F26) — so the next review over this document should expect a count near three and check
that each mark is still standing rather than quietly permanent.

### 6. What holds

- The state list in Section 4 gives each state an entry condition, not just a name, which is what made
  the transitions in Phase 1b checkable at all.
- Section 9 collects the cross-cutting rules in one place. Every one of them turned out to need work,
  and having them gathered is why the sweep in F22 could run against them as a set.
- Section 13 declares its own open items, including the capacity question, rather than leaving them
  for a reviewer to discover.

### Overall readiness

**Needs another iteration.** The design's shape is sound and the defects cluster in three areas —
the offline boundary, the deposit and pickup step sequences, and the end of the parcel's life — so one
focused pass closes most of them.

---

## Finding ledger

Status is the same on every row: this pass was read-only by instruction, and no fix was written into
the document.

| ID | Kind | Category | Status |
|---|---|---|---|
| F1 | defect | unclear-owner (actors) | not applied — review-only pass |
| F2 | defect | boundary-issue (composition) | not applied — review-only pass |
| F3 | defect | missing-scenario (state-space) | not applied — review-only pass |
| F4 | defect | missing-scenario (state-space) | not applied — review-only pass |
| F5 | defect | missing-rule (invariant) | not applied — review-only pass |
| F6 | defect | partial-success-risk (atomicity) | not applied — review-only pass |
| F7 | defect | missing-rule (invariant) | not applied — review-only pass |
| F8 | defect | missing-outcome-check (postcondition) | not applied — review-only pass |
| F9 | defect | missing-prerequisite (precondition) | not applied — review-only pass |
| F10 | defect | missing-prerequisite (precondition) | not applied — review-only pass |
| F11 | defect | unclear-recovery (rollback) | not applied — review-only pass |
| F12 | defect | no-exit (dead-end) | not applied — review-only pass |
| F13 | defect | stuck-state (liveness) | not applied — review-only pass |
| F14 | defect | stuck-state (liveness) | not applied — review-only pass |
| F15 | defect | unenforceable-promise (discharge) | not applied — review-only pass |
| F16 | defect | unenforceable-promise (discharge) | not applied — review-only pass |
| F17 | defect | direct-contradiction (contradiction) | not applied — review-only pass |
| F18 | defect | direct-contradiction (contradiction) | not applied — review-only pass |
| F19 | defect | internal-conflict (consistency) | not applied — review-only pass |
| F20 | defect | internal-conflict (consistency) | not applied — review-only pass |
| F21 | defect | missing-rule (invariant) | not applied — review-only pass |
| F22 | defect | missing-rule (invariant) | not applied — review-only pass |
| F23 | defect | missing-scenario (state-space) | not applied — review-only pass |
| F24 | defect | missing-scenario (state-space) | not applied — review-only pass |
| F25 | defect | undefined-path (transitions) | not applied — review-only pass |
| F26 | defect | hard-to-monitor (observability) | not applied — review-only pass |
| F27 | defect | hard-to-monitor (observability) | not applied — review-only pass |
| F28 | defect | missing-outcome-check (postcondition) | not applied — review-only pass |
| F29 | defect | undefined-path (transitions) | not applied — review-only pass |
| F30 | recommendation · now | hard-to-monitor (observability) | not applied — review-only pass |
| F31 | defect | missing-prerequisite (precondition) | not applied — review-only pass |
| F32 | recommendation · later | confusing-for-users (cognitive-load) | not applied — review-only pass |
| A1 | acknowledged | missing-scenario (state-space) | the document's own known issue |
| A2 | acknowledged | unenforceable-promise (discharge) | the document's own known issue |
| A3 | acknowledged | missing-scenario (state-space) | the document's own known issue |

Totals: 32 findings — 30 defects and 2 recommendations — plus 3 acknowledged gaps, which carry no
kind and are not counted as findings.
