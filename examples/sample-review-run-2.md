# Product Prover review — Cedarline Lockers, release 2

- **Skill:** product-prover, edition `1.0.0-standalone` (as stated in `SKILL.md` metadata).
- **Date:** 2026-08-06.
- **Document reviewed:** `editions/product-prover/examples/sample-spec.md` — "Cedarline Lockers — parcel pickup, release 2 (sample spec)".
- **Mode:** full review (default), all phases.

What the project running this review does not have, so the rules naming them read as advice here and
the checks are recorded as not run rather than passed:

- no pre-merge check is in reach, so nothing applies the defects mechanically;
- no test suite is in reach, so no sweep leans on a test row;
- no readability review and no design-consistency review ran, so the passes that belong to them are
  named where they would pick something up and left there;
- the project keeps no surface registry, so the cross-surface policy uniformity sweep takes an N/A
  verdict on its enumeration half throughout, with the reason recorded in every affected cell;
- the rewrite merge gate stands down by name: this document arrived on its own and carries no old
  side to judge a delta against.

Diagrams: this review is written into a file, which renders no visuals. Per the skill's own rule the
record carries the prose lists and leaves any diagram to a session that can show one.

Finding IDs `F1`–`F30` are numbered once across the pass in the order written. Acknowledged gaps
carry `A1`–`A3` and no kind.

| ID | Kind | Applied / rejected |
|---|---|---|
| F1–F30 | see each finding's tag | not applied — this pass is read-only over the sample document, and no fix was written into it |
| A1–A3 | acknowledged, no kind | n/a |

---

## Phase 0 — Triage

`TRIAGE: PROCEED` — a feature spec with named entities, a four-state parcel lifecycle, stated
transitions, actors, and cross-cutting rules; enough material to extract a model and argue with it.

Three triage notes carry into everything below.

**A partly-shipped system, with no pins.** Section 1 says "Release 2 adds the pickup window and the
expiry sweep to the release 1 deposit flow", so the deposit flow in Section 5 and parts of Section 9
describe something already built. The document carries no `file:line` pins, and the code is out of
reach altogether: this is a fictional practice document with no repository behind it. Every finding
that touches the release-1 deposit flow is therefore conditional on the document being current. I
cannot flag any section as possibly-removed, because there is no code or test to check a surface
against; that check is recorded here as not runnable, with that reason.

**Not an architecture document.** It names no nodes, no placement, and no runtime view. The
architecture lens does not run, and its seven checks are recorded as not applicable rather than
clean.

**The interpretation rule.** Two places below sharpen a standard past the words the author used —
the reading of the 72-hour window as running from door-shut (Phase 1), and the reading of "receives
its pickup code" as delivery rather than generation (F10). Both are marked as my reading, and
neither is applied as though the author had written it.

## Opening assessment

Cedarline is specifying a physical custody handoff: a courier locks a parcel in a box, a code travels
to a stranger by SMS, and that stranger has a bounded window to take the parcel out. The model is
admirably small — three entities, four parcel states, one page of cross-cutting rules — and small is
the right instinct for a system whose operators stand in supermarkets. Section 13 is the document's
best habit: it names its own holes out loud instead of hiding them, and Section 12 takes a real
position on offline operation rather than assuming the network.

Two things need attention before anyone builds this. First, the whole design infers physical facts
from door events — a shut door means a parcel went in, a shut door means a parcel came out — and
nothing senses the parcel, so both of the state model's load-bearing transitions can fire on an empty
compartment or a full one (F8). Second, the lifecycle runs out of road at Expired: "An expired parcel
is returned to the carrier" is a sentence about the world, not a transition, and nothing in the model
ever frees the compartment again (F1, F2). A bank of forty boxes silently loses capacity every day
the sweep runs.

Overall confidence: **needs significant rework**. The skeleton is sound and the rework is mostly
writing down owed answers rather than redesigning anything, but there are too many of them to call
this one more iteration.

## Phase 1 — The model

### 1a. Entities and relationships

- **Parcel** — one shipment, identified by a tracking number. Sits in at most one Compartment while
  Stored; carries one Pickup code. Arrives into the system from a Carrier manifest.
- **Compartment** — one lockable box, free or occupied. Holds at most one Parcel at a time (Section
  9). Belongs to one Bank (inferred — the document never states the containment).
- **Pickup code** — six digits, tied to one Parcel and one Compartment. Its uniqueness scope is
  unstated.
- **Bank** *(inferred)* — a set of Compartments at one site, with a keypad, an event log, and a
  network link. Load-bearing in Sections 8, 9, 11, and 12, and absent from the Section 3 entity list.
- **Event log** *(inferred)* — held by the Bank, written at every deposit and every opening, synced
  to Cedarline when the link returns. No reader, retention, or schema stated.
- **Carrier** *(inferred, external)* — sends the manifest that creates a Parcel, and receives an
  expired Parcel back.

### 1b. States and transitions

States of Parcel:

1. **Registered** — entered when the carrier's manifest arrives; exits to Stored (courier deposit).
   No other exit stated. A parcel that never arrives has no path out.
2. **Stored** — entered at deposit, when Cedarline marks it Stored; exits to PickedUp (recipient
   shuts the door) or to Expired (nightly sweep, once the 72-hour window has run out).
3. **PickedUp** — entered when the recipient closes the compartment door. Terminal, stated as such.
4. **Expired** — entered by the 03:00 sweep. **No exit stated.** "Returned to the carrier" names no
   state, no actor, and no transition.

States of Compartment:

1. **Free** — exits to Occupied when the bank opens it for a deposit and the courier shuts the door.
2. **Occupied** — exits to Free when a recipient closes the door after pickup (Section 6). No exit
   stated for the expiry path, and none for an operator removing a parcel (Section 8).

### 1c. Actors and actions

- Send manifest, creating a Registered parcel — Carrier (external system).
- Scan badge, scan tracking number, place parcel, shut door — Courier.
- Open a free compartment at deposit — locker bank (automated).
- Mark Stored, generate the pickup code, send the SMS, retry a failed send — Cedarline (automated).
- Enter code, open compartment, take parcel, shut door — Recipient.
- Run the expiry sweep at 03:00 and move parcels to Expired — Cedarline (automated).
- Return an expired parcel to the carrier — **initiator not stated**.
- Empty the compartment holding an expired parcel — **initiator not stated**.
- Open any compartment with a service badge — Operator.
- Read the operations dashboard — **audience not stated**.

### 1d. Composition and boundaries

Four parts, with three seams between them:

- **Locker bank** — hardware plus local logic: badge reader, scanner, keypad, doors, event log.
  Stated to keep working with its network link down.
- **Cedarline central** — parcel state, code generation, the 03:00 sweep, the dashboard.
- **SMS gateway** — third party, accepts a send request and reports delivery asynchronously.
- **Carrier** — external, upstream at the manifest and downstream at the return.

The bank ↔ central seam is the one the document leans on hardest and writes least about: which side
decides that a code is valid, which side holds the clock the 72-hour window runs on, and what
crosses when a bank comes back online.

### What I assumed

- I read "Cedarline" in Section 5 as the central service, distinct from the locker bank hardware,
  because Section 12 lets the bank keep working while the link to something else is down.
- I read the 72-hour window as running from the door-shut moment at deposit, not from the manifest
  arriving. The document says "72 hours from deposit" and never fixes which instant "deposit" names.
  That is my reading, and it is the more favourable of the two.
- I treated Bank and Event log as entities even though Section 3 lists neither, because Sections 8
  through 12 cannot be read without them.
- I treated billing, parcel damage, hardware provisioning, and how banks are installed as
  out-of-scope, following Section 13 for damage and the document's silence for the rest.
- I found no authoritative surface for locker-bank and compartment inventory named in this doc. If
  one exists in the product, none of the operations here register with it.
- I did not check any claim against code or tests. There are none in reach, so nothing below rests
  on a primary source beyond the document's own sentences.

## Phase 2 — Structural issues in the model

F1 — Expired is a dead end: the parcel's last stated state has no way out

> "An expired parcel is returned to the carrier." — Section 7. Expiry

That sentence describes something happening in the world, and the model gives it no transition, no
state, and nobody who performs it. A recipient who arrives on day four finds their parcel gone from
the system's point of view and present in the box; an operator asked "where is parcel X" reads
Expired and has no record of whether it left the bank, sat in a van, or is still behind door 12. Once
the carrier has it back, the parcel is Expired forever in Cedarline, and no query can separate
"returned last month" from "expired overnight and still in the compartment".

Add a fifth state, **Returned**, entered when an operator scans the parcel out of the bank, and state
that Expired exits only that way. Write the operator's scan-out as the transition, with the
compartment freed and the event logged in the same step.

`defect · no-exit (dead-end)`

F2 — Nothing frees a compartment after expiry, so a bank leaks capacity every night

> "The expiry sweep runs daily at 03:00 and moves every parcel whose pickup window has run out into
> Expired." — Section 7. Expiry

The sweep changes parcel state and touches no compartment. Section 6 frees a compartment on one path
only, the recipient closing the door after pickup. So an expired parcel's box stays occupied with no
stated way back to free, and the dashboard's "compartments free" count (Section 11) drops
permanently by one per expiry. At a bank of forty boxes with two expiries a week, capacity reaches
zero in five months, and the first symptom an operator sees is couriers reporting that deposits are
refused at a bank the dashboard says is half empty.

Make the compartment's release part of the scan-out transition proposed in F1, and state the
invariant that a compartment is free exactly when no parcel in a non-terminal state names it. Add the
per-bank count of compartments occupied by expired parcels to the dashboard, so the leak is visible
before it is total.

`defect · missing-scenario (state-space)`

F3 — An operator can open any compartment, and nothing says what that does to the parcel or the box

> "An operator with a service badge can open any compartment in a bank, so a jammed door, a parcel
> left by mistake, and a cleaning round are all serviceable on site." — Section 8. Operator servicing

Two of the three named cases move a parcel physically — a parcel left by mistake gets taken out, a
cleaning round empties boxes — and neither has a state transition. The operator removes a parcel and
the system still reads Stored, running its window; the pickup code still opens an empty box for a
recipient who then rings support and is told their parcel is in compartment 12. The sweep later
expires a parcel that has been on a van for two days, and the dashboard counts it as stored the whole
time.

Split Section 8 into three named operator actions with their state effects: unjam (no state change),
scan a parcel out (parcel to Returned or a new **Withdrawn** state, compartment freed, code
invalidated), and open an empty compartment (no state change). Require the parcel scan on any open
that ends with the operator holding a parcel, so the physical move and the state move are one action.

`defect · missing-scenario (state-space)`

F4 — Bank is load-bearing from Section 8 onward and is not in the entity list

> "**Compartment** — one lockable box in a bank. A compartment is free or occupied." — Section 3.
> Entities

Bank appears in the compartment's own definition and then carries the event log (Section 9), the
offline behaviour and the sync (Section 12), the dashboard's grouping (Section 11), and the operator's
scope (Section 8). Because it is never an entity, nothing states that a compartment belongs to exactly
one bank, or whether an operator's service badge is scoped to one bank or to all of them. A reader
building the data model has to invent the containment, and two readers will invent it differently.

Add **Bank** to Section 3 with its identifier, its relationship to Compartment (one bank holds many
compartments, each compartment in exactly one bank), and the two things it owns: the event log and
the network link. Then say whether a service badge is scoped per bank, per region, or globally.

`recommendation · now · boundary-issue (composition)`

F5 — Two live parcels in one bank can hold the same six-digit code

> "**Pickup code** — a six-digit code tied to one parcel and one compartment." — Section 3. Entities

Nothing requires codes to differ from each other. A six-digit code drawn at random collides with one
of forty live codes in a bank roughly once in twenty-five thousand deposits, which a busy network
reaches in weeks. On a collision the keypad has two compartments matching one code, and Section 6
says only "The bank opens the compartment holding that parcel" — there is no "that parcel" to speak
of. The recipient takes a stranger's parcel, both parcels are recorded as picked up by the code that
opened the door, and the event log shows one clean pickup.

State the uniqueness invariant and its scope: no two parcels with a live pickup code in the same bank
hold the same code. Generate codes by drawing against the bank's live set rather than at random, and
make the code's release back to the pool part of the transition that ends the window. If uniqueness
is meant to be global rather than per bank, say that instead — my preference is per bank, since a
code is only ever typed on one bank's keypad and a global set exhausts far sooner.

`defect · missing-rule (invariant)`

## Phase 3 — Property analysis

### 3a. Safety — things that must never happen

F6 — Deposit is one sentence covering four steps, with no behaviour stated between them

> "Cedarline then marks the parcel Stored, generates a pickup code, and sends the code to the
> recipient by SMS." — Section 5. Deposit

The courier has already shut the door, so the physical half is irreversible while three system steps
remain. If code generation fails after the state flip, the parcel is Stored with a running 72-hour
window and no code exists; the recipient is sent nothing, the sweep expires a parcel that was never
collectable, and the courier saw a completed deposit and left. If the SMS send fails to be accepted,
the same shape holds one step later.

Make the code's existence a precondition of Stored: generate the code before the door-shut event
flips state, and state that a parcel with no code enters no Stored state and starts no window. Write
the compensating action for a generation failure as an operator alert naming the bank and the
compartment, since the parcel is physically locked away and only an operator can reach it.

`defect · partial-success-risk (atomicity)`

F7 — The courier's badge is scanned and nothing says what a bad badge does

> "The courier scans their badge, scans the parcel's tracking number, and the locker bank opens a
> free compartment." — Section 5. Deposit

The badge is the only authentication on the deposit path, and the document writes a refusal rule for
the tracking number in the very next paragraph while writing none for the badge. So the reader cannot
tell whether an expired badge, a revoked badge, or no badge at all stops the deposit. Read one way,
anyone who scans a valid tracking number opens a compartment; read the other way, a courier with a
badge that expired overnight stands at a bank with a parcel and no stated outcome, and calls support.

Write the badge check as a precondition beside the tracking-number rule: a badge that is unknown,
expired, or revoked is refused at the scan and the bank opens no compartment. Name what the courier
sees at that refusal, and state whether the refusal is logged.

`defect · missing-prerequisite (precondition)`

F8 — Door events stand in for physical facts, on both of the model's load-bearing transitions

> "The courier puts the parcel in and shuts the door." — Section 5. Deposit
>
> "Closing the door marks the parcel PickedUp and the compartment free." — Section 6. Pickup

Nothing in Section 3 senses a parcel. Both directions therefore run on an unchecked assumption. A
courier who shuts an empty door produces a Stored parcel with a code, an SMS, and a running window
for a parcel that never entered the bank; the recipient arrives, opens an empty box, and Cedarline's
record says the parcel was there. A recipient who opens the door, sees the wrong parcel, and closes
it again produces PickedUp with the parcel still inside and the compartment marked free — and the
next courier is sent to that same compartment, where Section 9's one-parcel rule breaks physically
with no software able to notice. This is one class with two instances, and Section 9's "A pickup code
opens one compartment and stops working once the parcel leaves it" is a third: the system cannot
observe the parcel leaving, so that rule can never be evaluated as written.

Pick the physical evidence and write it into the transitions: either state that each compartment has
a presence sensor and make the sensor reading the precondition of Stored and the postcondition of
PickedUp, or state plainly that Cedarline infers occupancy from door events and name the reconciliation
that catches the drift — an operator audit round with a stated cadence, and a per-bank mismatch count
on the dashboard. My preference is the sensor on new banks and the audit round as the interim answer
for banks already in the field. Then reword the Section 9 rule to key on the transition the system
can actually see.

`defect · unenforceable-promise (discharge)`

F9 — The stated 72-hour window is really 72 to 96 hours, because the sweep runs once a day

> "The pickup window is 72 hours from deposit." — Section 6. Pickup
>
> "The expiry sweep runs daily at 03:00 …" — Section 7. Expiry

A parcel deposited at 04:00 on Monday passes 72 hours at 04:00 on Thursday and is not touched until
03:00 on Friday, so it stays collectable for 95 hours. A parcel deposited at 02:00 gets almost exactly
73. Two recipients told the same thing get windows a day apart, and a recipient who arrives at hour 80
and collects a parcel the SMS said had expired will not complain — but a recipient told 72 hours who
arrives at hour 71 and finds an expired parcel, because a manual sweep was re-run, will. The support
line cannot answer "was I in time" from the stated rule.

Decide which number is the promise and make the other follow it. Two options: (a) keep the daily
sweep and state the window as "until 03:00 following 72 hours after deposit", which is honest and
what the recipient's SMS should then say; (b) expire on the exact 72-hour mark by scheduling per
parcel, with the daily sweep kept as a backstop for anything the scheduler missed. I prefer (b), since
(a) hands a variable promise to the recipient and makes every capacity forecast a range.

`defect · internal-conflict (consistency)`

F10 — The one-minute code promise contradicts the retry schedule, and "receives" is doing two jobs

> "Every parcel receives its pickup code within one minute of deposit." — Section 9. Stated rules
>
> "Cedarline retries a failed send three times, at one minute, five minutes, and fifteen minutes." —
> Section 10. Notification

The retry schedule reaches sixteen minutes past the send, and the third retry alone falsifies the
one-minute rule. Read as generation, the rule is cheap and true; read as delivery, it is a promise
over a third-party gateway that reports asynchronously, which Cedarline cannot keep and cannot even
measure at the one-minute mark. I read it as delivery, because "receives" names the recipient — that
is my reading, and if generation was meant, the rule is stated on the wrong actor. Today a recipient
whose first send fails is inside a documented guarantee that the notification section openly plans to
break.

Split the rule in two. Write the internal one as a precondition Cedarline controls: "A pickup code
exists before the parcel enters Stored" — which F6 also asks for. Write the external one as an
observable target with its measuring point: "the send request is accepted by the gateway within one
minute of deposit, measured at Cedarline's outbound call", and give it the watcher that fails past
that number. Delete "receives", since it names an event Cedarline never sees.

`defect · direct-contradiction (contradiction)`

F11 — "Only the recipient can open" and "an operator can open any compartment" cannot both hold

> "Only the recipient can open a compartment holding a parcel." — Section 6. Pickup
>
> "An operator with a service badge can open any compartment in a bank …" — Section 8. Operator
> servicing

These are two sentences on the same class of action, the second of which is a plain exception to the
first, and neither names the other. A reader implementing Section 6 as written builds a door that
refuses a service badge on an occupied compartment, and the first jammed parcel becomes a site visit
with a screwdriver. A reader implementing Section 8 as written builds a badge that opens everything
and quietly deletes the Section 6 guarantee, and nobody can say afterwards which reading shipped.
This is also a rule about a whole kind — who may open a compartment — written inside one member's
section while two sibling openers exist, the courier's deposit open and the operator's service open.

Lift the rule to a class clause of its own and enumerate its members: a compartment holding a parcel
opens to the pickup code for that parcel, to a service badge, and to nothing else — with the deposit
open listed as the third member and scoped to free compartments. State the operator case as a named
exception inside that clause rather than in a section two pages later.

`defect · direct-contradiction (contradiction)`

F12 — The bank checks six digits, never a person, and nothing limits the guessing

> "Only the recipient can open a compartment holding a parcel." — Section 6. Pickup

Identity is not a thing the keypad can read. What the bank verifies is possession of a code, which is
a different claim, and the document offers no attempt limit, no lockout, and no alerting. A bank with
forty live six-digit codes yields a hit roughly once in twenty-five thousand tries; a person at the
keypad entering a code every three seconds reaches that in about twenty hours, and a small keypad
robot reaches it overnight, in a supermarket, with no log line distinguishing the attack from a
forgetful recipient. The observable outcome is a parcel picked up by the code that was typed, correctly
recorded as a clean pickup.

Restate the rule as what the system can prove: "a compartment holding a parcel opens to a valid live
pickup code for that parcel, and to a service badge". Then add the controls that make possession
mean something — a per-compartment cap of five failed entries before that compartment's code is
frozen and reissued, a per-bank rate limit on failed entries, and an operator alert past the bank
threshold. Whether Cedarline also wants a second factor on high-value parcels is a business call, and
it belongs in the open questions rather than here.

`defect · unenforceable-promise (discharge)`

### 3b. Liveness — things that must eventually happen

F13 — A registered parcel that never arrives stays Registered forever

> "**Registered** — the carrier has told Cedarline the parcel is coming. Entered when the carrier's
> manifest arrives." — Section 4. Parcel states

Registered has exactly one exit, the deposit. Carriers lose parcels, reroute them, and cancel them,
and none of those has a path in this model. The record accumulates: after a year, the Registered set
holds every parcel that was ever announced and never deposited, mixed with the ones announced an hour
ago. An operator asked "is parcel X coming" cannot tell a live expectation from a two-year-old ghost,
and any report counting expected arrivals per bank is wrong by an amount that only grows.

Give Registered a time bound and a second exit: a registered parcel not deposited within a stated
number of days moves to **Lapsed**, and the manifest feed's cancellation message moves it there
immediately. State the number, and state whether a lapsed parcel can be deposited later or must be
re-registered — my preference is that a deposit against a Lapsed tracking number is refused at the
scan, which reuses the rule already in Section 5.

`defect · stuck-state (liveness)`

F14 — The retry schedule runs out and the document stops there

> "Cedarline retries a failed send three times, at one minute, five minutes, and fifteen minutes." —
> Section 10. Notification

After the third failure nothing is stated. The parcel is Stored, the window is running, the code
exists, and the recipient has never heard of any of it — a wrong phone number on the manifest, a
number that stopped accepting SMS, or a gateway outage of more than sixteen minutes all land here.
Three days later the sweep expires the parcel, the operator returns it to the carrier, and the first
person to learn anything went wrong is the sender, weeks later, through a carrier complaint. Nobody
at Cedarline is paged, and the dashboard shows an ordinary expiry.

Write the terminal branch: after the third failed retry, the parcel is flagged **undelivered-code**,
an operator alert fires naming the bank, the compartment, and the tracking number, and the 72-hour
window is suspended until a code reaches the recipient. State whether Cedarline may re-send to a
corrected number, and who is allowed to correct it. Suspending the window is my preference over
letting it run, because the recipient never had the chance the window is meant to measure.

`defect · stuck-state (liveness)`

### 3c. Whether the spec can be enforced

Two findings above are this section's, and they are not repeated here: F8 (the state model asserts
physical facts no stated component can observe) and F12 (an identity claim over a possession check).
One counterexample worth naming beyond them: Section 9's "A pickup code opens one compartment and
stops working once the parcel leaves it" has no evaluable trigger, since "leaves it" is exactly the
event F8 shows nothing detects. That rule is folded into F8's proposed rewording rather than filed
twice.

### 3d. Internal consistency

F15 — The dashboard's three counts and the bank's real occupancy have no tying rule

> "The operations dashboard shows, per bank: compartments free, parcels stored, and parcels expired
> today." — Section 11. Reporting

Free compartments and stored parcels are two views of one fact, compartment occupancy, and nothing
states how they relate. With F2 standing, they cannot even be reconciled: expired parcels occupy boxes
and are counted in neither number, so free plus stored is less than the bank's size by a figure the
dashboard never shows. A dispatcher reads eleven compartments free at the Kings Cross bank, routes a
courier with fourteen parcels, and the courier is refused at box twelve with no explanation the
document provides. "Expired today" compounds it, because a parcel expired last Tuesday and still in
its box appears in no count at all.

State the tie as an invariant the dashboard is derived from: for every bank, compartments free plus
compartments holding a parcel in any non-terminal state equals the bank's compartment count. Add a
fourth figure, compartments holding an expired parcel, and derive all four from one occupancy query
rather than from three independent ones.

`defect · missing-rule (invariant)`

### 3e. Generative stress-testing

`reference/stress-lenses.md` was read before any finding in this subsection was written. Findings
F16–F25 come from it. Both tiers ran: the five mandatory sweeps, each of which owes a verdict in the
table at the end of this phase, and the imaginative probes, which owe none.

#### Sweep 1 — declared cross-cutting laws

Section 9, "Stated rules", is this document's declared-laws section: four rules that hold across every
surface, recognizable by content rather than by its title. Section 12 adds two more. The per-law walk
runs against those six.

F16 — Six cross-cutting rules and not one names the thing that fails when it is broken

> "- Every parcel receives its pickup code within one minute of deposit.
> - A compartment holds one parcel at a time.
> - A pickup code opens one compartment and stops working once the parcel leaves it.
> - Every deposit and every opening is written to the bank's event log." — Section 9. Stated rules

Every one of these is stated as a fact about the world with nothing behind it: no named check, no
test row, no named reviewer, no alert. The consequence is that they degrade invisibly. The one-parcel
rule breaks physically the first time F8's empty-door pickup fires and no component is looking; the
one-minute rule breaks on every third retry and nothing counts it; the log rule breaks on a bank whose
sync never completes and nobody is told. An operator's first evidence of any of the six is a customer
complaint, which arrives weeks after the rule stopped holding. This is one class with six instances,
and Section 12's two non-functional rules ("A bank works while its network link is down", "Keypad
entry to door open takes under two seconds") are the fifth and sixth.

Add a column to Section 9 and Section 12 naming each rule's enforcer, and pick one of three per rule:
a named mechanical check that fails in continuous integration, this review where the violation pins to
a sentence, or a named reviewer where only judgment can decide. Concretely: the one-parcel rule gets a
nightly per-bank reconciliation job with its alert; the code-uniqueness rule from F5 gets a database
constraint on the live-code set; the two-second rule gets a per-open latency metric with a stated
percentile and a threshold alert; the log rule gets a sync-lag metric per bank. Where a rule ends up
with no enforcer worth building, say so in a sentence and mark it as aspiration rather than as a rule.

Note on the "test per surface" demand: no test matrix is in reach for this document, so this sweep is
the only reader of these six rules, and the untested-surface check is recorded as not runnable.

`defect · missing-rule (invariant)`

F17 — The log law covers doors, and the state changes that happen without a door are invisible

> "Every deposit and every opening is written to the bank's event log." — Section 9. Stated rules

Three of the system's most consequential events involve no door and are therefore written nowhere:
the sweep moving a parcel to Expired, the generation of a pickup code, and the exhaustion of the SMS
retries. The log also lives on the bank, so a central action like the sweep has no natural place in
it at all. When a recipient calls to say their parcel vanished, the operator can see that a door
opened at 14:02 and cannot see who held the badge, why the sweep expired the parcel at 03:00, or
whether a code was ever sent. Section 8's operator opens land in the log as bare openings, with no
operator identity and no reason recorded, so a parcel taken during a cleaning round is
indistinguishable from a pickup.

Restate the law over state changes rather than over doors: every transition of a parcel or a
compartment is written to an event record, with the actor, the trigger, and the timestamp. Keep the
bank's local log for door events so it survives an offline period, and add a central record for the
sweep, code generation, and send outcomes. Require the operator's badge identity and a reason code on
every service open, chosen from the three cases Section 8 already names.

`defect · hard-to-operate (ops-ux)`

#### Sweep 2 — edge-condition completeness

F18 — The SMS's pending, arrived, and failed states are observable nowhere

> "The gateway accepts a send request and reports delivery asynchronously." — Section 10.
> Notification

Delivery reports come back and the document never says where they land. The dashboard (Section 11)
shows three counts, none about notification; the parcel's four states say nothing about its code; the
event log covers doors. So a support agent taking a call from a recipient who says "I never got a
code" has no screen that distinguishes never sent, sent and pending, delivered, or failed three times
— and neither does the operator standing at the bank. The reports the gateway spends money producing
are consumed by nothing.

Add a notification status to the parcel with exactly those four values — not-sent, pending, delivered,
failed — set from the gateway's asynchronous report, shown on the parcel's record and counted per bank
on the dashboard as "codes undelivered". State how long a pending status may stand before it is read
as failed, since the gateway's report may never arrive at all.

`defect · hard-to-monitor (observability)`

F19 — "A bank works while its network link is down" names no duration and no degraded behaviour

> "A bank works while its network link is down, and it syncs events when the link returns." — Section
> 12. Non-functional

The guarantee is scoped to one named part of its domain, the link being down, and the remainder is
silent at both ends. How long: an hour, a week? What "works" covers: can a courier deposit into an
offline bank, when the code is generated centrally and sent by a gateway the bank cannot reach? Can a
recipient pick up, when validating a code needs a code the bank may not have? The two-second keypad
guarantee names no condition band either, so it is unclear whether it holds offline. Concretely, a
courier at a bank offline since yesterday shuts a door and nobody can say whether a parcel is Stored,
whether an SMS went out, or what the courier's handheld showed. When the link returns and the bank
syncs, that deposit lands in central state hours late, after the sweep has already run.

State the offline contract as a table of the three surfaces against the two link states: deposit,
pickup, and operator open, each reading allowed or refused while offline, with what the person at the
bank sees. Name the maximum offline period a bank tolerates before it refuses deposits, and say
whether the two-second guarantee is scoped to the online band. My preference is that pickup stays
allowed offline against a code cached at deposit and deposit is refused offline, because a deposit
offline cannot produce the code the whole flow depends on.

`defect · missing-scenario (state-space)`

#### Sweep 3 — cross-surface policy uniformity

The enumeration half of this sweep is not runnable: the project keeps no surface registry, so there is
no list to check a clause's members against. That N/A verdict is recorded in every cell of the
uniformity column below, with that reason. The half that reads a kind-general rule out of its own
sentence did run, and it produced F11 above and F20 here.

F20 — The deposit scanner has a refusal rule and the pickup keypad has none

> "A parcel whose tracking number is unknown to Cedarline is refused at the scan, and the bank opens
> no compartment." — Section 5. Deposit

That is an error contract for a whole kind — input rejected at a bank's reader — written on one
member while the sibling member, the keypad in Section 6, has no such sentence. Section 6 states only
what happens when the code is right. A recipient who mistypes a digit, arrives on day five with an
expired code, or reuses a code after collecting gets no stated behaviour, so three quite different
situations may render as the same blank screen. The recipient cannot tell "you typed it wrong, try
again" from "your parcel is gone", stands at the bank retyping, and calls support with no information
either of them can act on.

Write the keypad's refusal rule beside the scanner's, distinguishing four cases with the message each
one shows: unknown code, code for a parcel already picked up, code for an expired parcel, and a
compartment the bank cannot open. State that every refusal is logged with the case, so F17's record
can count them.

`defect · missing-scenario (state-space)`

#### Sweep 4 — lifecycle

The lifecycle walk covers transition payload, entry symmetry, entry state, paired-transition symmetry,
persistence and versions, and scenario entry and exit. F1 and F2 above came out of the paired-transition
read on free/occupied, whose forward direction is written and whose reverse is written on one path
only. Two further findings follow.

F21 — The compartment opened at deposit and never shut has no answer

> "The courier scans their badge, scans the parcel's tracking number, and the locker bank opens a free
> compartment." — Section 5. Deposit

The open is stated and the payload that carries across it is not: how long the door stays open, what
holds the compartment reserved meanwhile, and what happens if the courier is called away, drops the
parcel, or walks off. The parcel stays Registered, the compartment is neither free nor occupied by
the document's own two-value definition, and the box stands open in a supermarket overnight. Anyone
passing takes whatever is inside, and the event log shows one opening and no deposit.

State the open's lifetime and its reverse: the compartment is reserved at the scan and the door
auto-locks after a stated number of seconds, returning the compartment to free if no parcel was
detected or the deposit was not completed. Name what the courier sees when the reservation lapses, and
add a third compartment value, **reserved**, so the two-state definition in Section 3 stops being
false during a deposit.

`defect · undefined-path (transitions)`

F22 — The 03:00 sweep and a pickup can act on the same parcel, and no side is named the winner

> "The expiry sweep runs daily at 03:00 and moves every parcel whose pickup window has run out into
> Expired." — Section 7. Expiry
>
> "A bank works while its network link is down, and it syncs events when the link returns." — Section
> 12. Non-functional

Two shapes, one root. Online: a recipient types a valid code at 02:59:58, the door opens, and the
sweep moves the parcel to Expired while the door is still open — the recipient walks away with a
parcel the system will report as returned to the carrier, and the compartment is freed by a pickup
event applied to an expired parcel. Offline: a bank out of contact for two days validates a cached
code and opens a door for a parcel central marked Expired last night and an operator may already have
scanned back to the carrier; when the link returns, the sync delivers a PickedUp event for a parcel
in a terminal state, and the document says nothing about which write survives.

Name the authority and the ordering. State that the parcel's state transitions are serialized per
parcel and that a pickup in progress blocks expiry — concretely, the sweep skips any parcel whose
compartment has been opened within a stated window and re-reads it on the next run. For the offline
case, state the conflict rule for late-arriving bank events: a PickedUp event arriving for an Expired
parcel wins and moves the parcel to PickedUp with a reconciliation flag, since the physical fact
outranks the scheduled one. Whichever rule is chosen, it has to be written down; today both sides
believe they are correct.

`defect · partial-success-risk (atomicity)`

#### Sweep 5 — unwritten seams

F23 — Two couriers at one bank can be sent to the same free compartment

> "… the locker bank opens a free compartment." — Section 5. Deposit

The bank is a shared surface and nothing in the document says only one person uses it at a time. Two
couriers arriving together — routine at a transport hub in the morning — each scan a badge and a
tracking number, and the selection of "a free compartment" is described as though it happens once.
With no reservation between the selection and the door shutting (F21), both can be pointed at
compartment 7, or the second can be pointed at a compartment the first has already filled but not yet
had marked Stored. The observable outcome is two parcels in one box, which breaks Section 9's
one-parcel rule physically, and one of the two tracking numbers is bound to a compartment holding
someone else's parcel.

State that compartment selection reserves the compartment atomically for one deposit session, and that
a second concurrent deposit at the same bank receives a different compartment or a refusal when none
is free. Say what the second courier sees while waiting, and how long a reservation is held before it
lapses, reusing the number from F21.

`defect · missing-scenario (state-space)`

F24 — A second manifest for a parcel already in the system has no stated effect

> "**Registered** — the carrier has told Cedarline the parcel is coming. Entered when the carrier's
> manifest arrives." — Section 4. Parcel states

Manifests are re-sent, corrected, and duplicated by every carrier feed I have seen, and the document
treats the arrival as a single event. Nothing says whether a repeat manifest for a tracking number
already Registered is ignored, whether it may update the recipient's phone number, or what it does to
a parcel that is already Stored with a live code. The plausible failure is a corrected phone number
arriving after deposit and being dropped, leaving the code sitting at the old number while the
document promises the recipient got it.

Write the manifest's idempotency rule: a manifest for a known tracking number in Registered updates
the recipient's contact details and changes nothing else; one for a parcel in any other state is
recorded and rejected, with an operator alert where the contact details differ. State whether a
contact change after deposit triggers a re-send of the existing code — I would re-send, since the
alternative is a guaranteed silent failure.

`recommendation · now · missing-scenario (state-space)`

#### Imaginative probes

The probes owe no verdict, and the class lens beside them owes the line under the verdict table.
Two produced findings — surface authority (F25) and interactive overlap, which is folded into F23, since the bank's shared keypad and shared compartment pool are the two
layers competing for one input. The class lens ran on F8 and on F16, and each of those findings names
its class and lists its instances rather than pointing at one spot. Reference integrity produced F24.
Three probes read clean here: approved-look clauses (the document encodes no approved exemplar),
false serialization (this is not a concurrency plan), and delivery separability (the document declares
no composition axis that adds runtime code).

F25 — Nothing crosses back to the carrier, and the carrier is where the recipient looks

> "An expired parcel is returned to the carrier." — Section 7. Expiry

The carrier is an authoritative surface for parcel status that this document names twice — it sends
the manifest that creates the parcel and receives the parcel back — and the seam is written in one
direction only. Nothing states that PickedUp or Expired is published back, so a recipient tracking
their parcel on the carrier's site after collecting it sees "at locker" indefinitely, and the carrier's
own support cannot tell a customer whether the parcel is in a box, on a shelf, or already back in
their network. The physical return has no message beside it either, so the carrier receives parcels
with no reconciliation against what Cedarline says it sent.

Write the outbound half of the seam: on every terminal transition, Cedarline publishes the tracking
number, the new state, and the timestamp to the carrier, and it names which side owns the message
format. For the physical return, state the handover record — a manifest of parcels scanned out, with
the carrier's acknowledgement — so both sides can reconcile. If release 2 is not building this,
record it as a known one-way seam rather than leaving the sentence in Section 7 to imply an
integration that does not exist.

`defect · boundary-issue (composition)`

### Coverage tables

CRUD coverage per entity:

| Entity | Create | Read | Update | Delete | Notes |
|---|---|---|---|---|---|
| Parcel | covered | partial | partial | missing | Created by manifest; read only as three aggregate counts, with no per-parcel lookup stated; no correction path for a wrong state; the exit at return is undefined (F1) |
| Compartment | missing | partial | partial | missing | Provisioning of a bank's compartments is unspecified; occupancy flips on two paths and never back after expiry (F2, F3) |
| Pickup code | partial | partial | missing | partial | Generated at deposit with no uniqueness rule (F5); read only by the recipient over SMS; no reissue path when the send fails (F14); "stops working" is unobservable (F8) |
| Event log entry | covered | missing | n/a | missing | Written per Section 9; no reader, no query, no retention, and no operator identity (F17) |
| Bank | missing | partial | missing | missing | Not an entity in the document at all (F4) |

Invariants per state:

| State | Invariants stated | Invariants missing |
|---|---|---|
| Registered | none | a bound on how long it may hold; a second exit for cancelled or lost parcels (F13) |
| Stored | the compartment holds one parcel at a time; the pickup window is 72 hours | a pickup code exists and is unique among live codes (F5, F6); the named compartment is occupied by this parcel and no other; the window's start instant; the window's suspension when no code was delivered (F14) |
| PickedUp | terminal | the parcel physically left the compartment (F8); the compartment is free exactly when no non-terminal parcel names it (F2) |
| Expired | none | an exit to a returned state (F1); the compartment's release (F2); no expiry while a pickup is in flight (F22) |
| Compartment free | free or occupied, one parcel at a time | the reserved value that exists during a deposit (F21); free plus occupied equals the bank's size (F15) |

Authorization per action:

| Action | Roles allowed | Granular check enforceable? | Notes |
|---|---|---|---|
| Deposit a parcel | Courier | partial | Badge scanned, with no stated check and no refusal path (F7) |
| Open a compartment holding a parcel | Recipient (Section 6) | no | The bank verifies six digits, not a person, and no attempt limit exists (F12) |
| Open any compartment | Operator | partial | Service badge with no stated scope, no reason recorded, and no identity in the log (F11, F17) |
| Run the expiry sweep | automated | n/a | No manual re-run is stated; if one exists it needs its own row |
| Read the operations dashboard | not stated | no | No audience, no per-bank scoping, and no rule on who sees which banks |
| Return a parcel to the carrier | not stated | no | No actor at all (F1, F2) |

### Surface × sweep verdicts

Every full review renders this table. Surfaces run down the side, the five mandatory sweeps across,
and each cell reads hit, clean, or N/A with its reason.

| Surface | Cross-cutting laws | Edge conditions | Policy uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| Deposit at the locker bank (§5) | hit (F16, F17) | hit (F19) | N/A — no surface registry | hit (F21) | hit (F23) |
| Pickup keypad (§6) | hit (F16) | clean | hit (F11, F20) — from the kind-general-rule read; the enumeration half is N/A, no surface registry | hit (F22) | hit (F23) |
| Expiry sweep (§7) | hit (F17) | hit (F9) | N/A — no surface registry | hit (F1, F2) | hit (F22) |
| Operator service open (§8) | hit (F17) | clean | hit (F11) — kind-general-rule read; enumeration half N/A, no surface registry | hit (F3) | clean |
| SMS send and retry (§10) | hit (F10, F16) | hit (F18) | N/A — no surface registry | hit (F14) | hit (F25) |
| Operations dashboard (§11) | clean | hit (F19) | N/A — no surface registry | clean | hit (F15) |
| Carrier manifest intake (§4) | clean | clean | N/A — no surface registry | hit (F13) | hit (F24) |
| Offline event sync (§12) | hit (F16, F17) | hit (F19) | N/A — no surface registry | clean | hit (F22) |

Class lens: swept — the door-event stand-in class (F8) and the unnamed-consequence class (F16).

## Phase 3.5 — Acknowledged gaps

These are the three items Section 13 raises itself. They are the author's own known issues, and this
pass files no new finding against them; each gets the second-order consequence the section does not
spell out.

A1 — A full bank has no deposit story, and the courier is standing there with a parcel

> "**TBD:** what the courier does when a bank has no free compartment at deposit time." — Section 13.
> Open items

The gap is larger than it looks, because F2 makes full banks a routine state rather than a rare one:
every expired parcel permanently removes a compartment until someone specifies its release. The
second-order effect is on the parcel's state, not just the courier's afternoon. A parcel that was
Registered and could not be deposited stays Registered with no record of the failed attempt, so
neither the carrier nor Cedarline learns that a bank is saturated until complaints arrive.

Two options. (a) Refuse at the scan with the same rule Section 5 already uses for an unknown tracking
number, log a **deposit-refused-full** event against the parcel and the bank, and alert operations at
a stated threshold of refusals per bank per day. (b) Add overflow routing, where the bank names a
nearby bank with capacity and the parcel's record follows. I prefer (a) for release 2, since (b) needs
inter-bank state this document does not have, and (a) at least makes saturation visible.

`acknowledged · missing-scenario (state-space)`

A2 — Code sharing is already possible and the document is deciding whether to admit it

> "**Open question:** should a recipient be able to hand their code to someone else, and does the spec
> need to say anything about it?" — Section 13. Open items

The design question is settled by F12 whether the author likes it or not: a six-digit code typed on a
public keypad is a bearer token, so sharing works today and no clause can stop it. What is genuinely
open is the liability wording and whether Cedarline wants a deliberate delegation path. The
second-order consequence sits in the dispute case: a recipient who says "I never collected this" and a
log showing a correct code entry leaves support with nothing, because the record cannot distinguish a
shared code from a stolen one.

Two options. (a) State sharing as permitted, with the code named a bearer credential in the recipient's
SMS and in the terms, which costs nothing to build. (b) Add a named delegation, where the recipient
nominates a collector and a second code is issued, which gives the log something to say in a dispute.
My preference is (a) for release 2 with the wording done properly, and (b) only if disputes turn out
to be common.

`acknowledged · unenforceable-promise (discharge)`

A3 — Damage is out of scope, and the state model has no place to put a damaged parcel

> "The refund path for a parcel damaged inside a compartment is out of scope for release 2." —
> Section 13. Open items

Deferring the refund path is reasonable. What the deferral does not cover is the parcel itself: an
operator who opens a compartment and finds a crushed parcel has no state to move it to and, per F3,
no transition for removing it either. So the out-of-scope decision quietly leaves an in-scope hole,
and the operator's workaround will be to let the parcel expire, which reports to the carrier as an
uncollected parcel and loses the damage entirely.

Keep the refund out of scope and add the state anyway: an operator scan-out with a reason code,
including **damaged**, reusing the transition F3 asks for. That costs one enum value now and preserves
the evidence the refund path will need later.

`acknowledged · missing-scenario (state-space)`

## Phase 4 — Human and operational factors

F26 — The SMS carries a code and nothing else the recipient needs

> "Cedarline then marks the parcel Stored, generates a pickup code, and sends the code to the
> recipient by SMS." — Section 5. Deposit

The message's content is never specified, and a bare six-digit code is not actionable. The recipient
does not learn which bank holds the parcel, which supermarket that is, which compartment, what the
deadline is, or what to do if the box will not open. Someone expecting two parcels gets two codes and
cannot tell them apart. The predictable outcome is a support call per deposit for anything but the
simplest case, and expiries caused by recipients who never worked out where to go — which the
dashboard then reports as ordinary expiries.

Specify the message body as a template with named fields: bank name and street address, compartment
number, the code, the exact deadline as a date and time (which F9's decision fixes), the parcel
reference, and a support contact. State the character budget and what is dropped first when a message
would split, and state the language rule for a recipient whose locale is known.

`defect · missing-outcome-check (postcondition)`

F27 — The document's four state names are the only vocabulary, and two surfaces show them to people

> "3. **PickedUp** — the recipient has opened the compartment and taken the parcel. Terminal." —
> Section 4. Parcel states

`PickedUp` and `Registered` are internal identifiers, and the document never states what words the
dashboard and the SMS use instead. That is a leak waiting to happen: the shortest path from this spec
to a screen is a status column rendering the enum, so an operator reads "PickedUp" and a support agent
reads it back to a customer. Section 11's own labels — compartments free, parcels stored, parcels
expired today — are good plain English, which shows the author's instinct is right and simply
unwritten as a rule.

Add a two-column table mapping each internal state to the words each audience sees: the operator's
dashboard, the recipient's SMS, and the courier's handheld. Keep the internal names in code and state
that no surface renders them directly.

`recommendation · now · confusing-for-users (cognitive-load)`

F28 — Section 5's first paragraph packs seven ordered steps into prose

> "The courier scans their badge, scans the parcel's tracking number, and the locker bank opens a free
> compartment. The courier puts the parcel in and shuts the door. Cedarline then marks the parcel
> Stored, generates a pickup code, and sends the code to the recipient by SMS." — Section 5. Deposit

This is the document's most important flow and its densest paragraph: seven steps, three actors, and
the ordering between them all carried by commas and one "then". A reader has to re-read it to work
out which actor does what, and — as F6 shows — the prose form is exactly what hid the fact that the
irreversible physical step sits in the middle with three system steps after it. A numbered list with
the actor on each step would have made that visible on the first read.

Rewrite the paragraph as a numbered list, one step per line, each opening with its actor. Keep the
refusal paragraph below it as prose, since it is a single rule rather than a sequence.

`recommendation · later · confusing-for-users (cognitive-load)`

F29 — One performance number, no watcher, and no ceiling on anything that grows

> "Keypad entry to door open takes under two seconds." — Section 12. Non-functional

It is the only number in the document, it names no measuring point and no percentile, and nothing
fails when it is missed. Everything else that scales is unbounded: how many banks the sweep walks at
03:00 and how long it may take, how many compartments a bank may hold, how many events an offline bank
buffers before it runs out of room, and how large the retry queue may grow during a gateway outage.
The failure mode is quiet — the sweep at a thousand banks starts overlapping its next run, and F22's
race becomes the normal case rather than the edge one.

State the ceilings explicitly, with numbers: compartments per bank, banks per region, the sweep's
budget as a wall-clock duration with the count it holds at, the bank's offline event buffer in events
and in days, and the retry queue's cap. Restate the keypad number with its measuring point and
percentile — for instance, the 99th percentile from the last keypress to the door lock releasing,
measured at the bank — and give it the watcher F16 asks for.

`recommendation · now · hard-to-operate (ops-ux)`

F30 — A phone number crosses to a third party and no clause says anything about it

> "**Notification service** — a third-party SMS gateway that delivers pickup codes." — Section 2.
> Actors

That seam moves personal data out of Cedarline, and the document never says where the number comes
from (presumably the carrier's manifest, which is never stated either), how long Cedarline holds it,
what the gateway is allowed to retain, or whether the code inside the message counts as a credential
worth protecting in transit. Neither security nor privacy is named anywhere in the document, not even
as an explicit skip, so a reader cannot tell whether they were considered and dropped or simply never
raised. The event log has the same silence: it records every opening at every bank, with no retention
period and no access rule.

Add a short section naming the answers: the phone number's source, its retention in Cedarline and its
contractual retention at the gateway, the event log's retention and who may read it, and whether the
pickup code may appear in logs or support tooling. Where any of these is genuinely out of scope for
release 2, write it as an explicit skip with that wording, so the next reader knows it was a decision.

`defect · boundary-issue (composition)`

## Phase 5 — Closing summary

### 1. Top three to fix before development

1. **F8** — the state model asserts physical facts nothing observes; pick sensors or a stated
   reconciliation before either transition is built, since F5, F15, and F23 all sit on top of it.
2. **F1 and F2** — Expired has no exit and no compartment release, so every bank loses capacity
   permanently; this is the release's own new feature failing to close its own loop.
3. **F11 and F12** — the authorization story is both self-contradicting and unenforceable as written;
   one clause naming who may open a compartment, plus an attempt limit, settles both.

### 2. Properties the document should state explicitly

Paste-ready sentences:

- "No two parcels with a live pickup code in the same bank hold the same code."
- "A parcel enters Stored only after a pickup code for it exists."
- "For every bank, the count of free compartments plus the count of compartments holding a parcel in
  a non-terminal state equals the bank's compartment count."
- "A compartment is free exactly when no parcel in a non-terminal state names it."
- "Every Expired parcel has a guaranteed path to Returned, and that transition frees its
  compartment."
- "Every Registered parcel reaches Stored or Lapsed within N days of its manifest arriving."
- "Every transition of a parcel or a compartment is written to an event record naming the actor, the
  trigger, and the timestamp."
- "A compartment holding a parcel opens to a valid live pickup code for that parcel, to a service
  badge, and to nothing else."

### 3. Open questions for the author

Only the four that inspection cannot settle:

1. Which side owns the physical return to the carrier — Cedarline's operators driving parcels back, or
   the carrier collecting from the bank? F1 and F25 both need that answer before they can be written,
   and it is a contract question rather than a design one.
2. Is the 72-hour window a commercial commitment to carriers, or an operational default Cedarline may
   vary per bank? F9's choice between the exact mark and the sweep boundary follows from that.
3. Does the deposit flow already shipped in release 1 behave as Section 5 describes? No code is in
   reach, so every finding touching Section 5 is conditional on that prose being current, and someone
   with the repository should confirm it before F6, F7, and F21 are worked.
4. Is a second factor on pickup ever wanted for high-value parcels, or is a bearer code the accepted
   model? F12 fixes the guessing problem either way, and this decides whether A2's delegation path is
   worth building.

### 4. Recommendations queued for a judgment call

Five, none blocking:

- **F4** — add Bank to the entity list and state the containment and the badge's scope.
- **F24** — write the manifest's idempotency and contact-update rule.
- **F27** — map internal state names to the words each audience sees.
- **F28** — rewrite Section 5's first paragraph as a numbered list.
- **F29** — state the scale ceilings and give the keypad budget a measuring point and a watcher.

### 5. Provisional defaults in the document

Zero. The document carries no `[default]` marks and no equivalent — nothing in it is written as a
behaviour standing until someone ratifies it. Section 13's three items are acknowledged gaps rather
than provisional defaults: they answer nothing, where a provisional default states a behaviour and
marks it unratified. Nothing to review here, and no oldest five to list.

### 6. What holds

- The state model is small enough to argue with. Four parcel states and three entities on one page is
  why every finding above could be pinned to a sentence rather than guessed at.
- Section 13 names the document's own holes out loud. That habit is rarer than it should be, and it
  is what let A1 through A3 be read as decisions in progress rather than as oversights.
- Section 12 takes a position on offline operation instead of assuming the network. The position is
  underspecified (F19), and having it at all is what makes the underspecification findable.

### Readiness

**Needs significant rework** — the skeleton is right and the volume of owed answers is too large for
one iteration: twenty-five defects, of which F1, F2, F8, F11, F12, and F22 each change how a
transition is written.
