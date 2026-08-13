# Product Prover sample response — compact conversation layer

`TRIAGE: PROCEED` — the document states actors, entities, states, transitions, rules, and failure
behaviour, so it supports a structural review.

## Verdict

Cedarline's main flow is easy to extract, and the document usefully separates its own open items.
The release is not ready to build. Its new expiry behaviour leaks compartment capacity, deposit joins
an irreversible physical act to three fallible system steps, and the authorization clauses conflict.
The detailed evidence is in `docs/review/2026-08-13-cedarline.md`. Overall readiness: **needs
significant rework**.

## Compact model

- Actors: courier, recipient, operator, carrier intake, notification service, expiry scheduler.
- Main parcel states: Registered → Stored → PickedUp or Expired.
- Review-derived surfaces: manifest intake, deposit scanner and door, pickup keypad and door, expiry
  sweep, operator service opening, text-message delivery, event sync, operations dashboard.
- Main boundary left unstated: which decisions belong to the locker bank while offline and which
  belong to Cedarline's central service.

## Top findings

F1 — Expiry permanently consumes a compartment

> "The expiry sweep ... moves every parcel whose pickup window has run out into Expired." — Section 7

A bank operator reaches the next morning with an Expired parcel still occupying its box. No actor,
deadline, or transition returns it to the carrier, and neither expiry nor return makes the
compartment free. Each expiry therefore reduces the bank's usable capacity until somebody performs
an undocumented repair.

Add a `Returned` state, name the actor and deadline for the return, and make that transition free the
compartment. State what the recipient and dashboard show while the parcel awaits return.

`defect · no-exit (dead-end)`

F2 — Deposit crosses an irreversible boundary with no partial-failure behaviour

> "Cedarline then marks the parcel Stored, generates a pickup code, and sends it through the
> notification service." — close paraphrase of Section 5

The courier can shut the door and leave before code generation or notification succeeds. The parcel
then occupies a compartment while the recipient has no usable code, yet its 72-hour window may
already be running. The courier sees a completed deposit and cannot recover it.

Make code existence a precondition of `Stored`. State the exact commit point, the state before it,
and the compensating action after a door closes but code generation fails.

`defect · partial-success-risk (atomicity)`

F3 — The authorization rule contradicts the operator path and cannot identify a recipient

> "Only the recipient can open a compartment holding a parcel." — Section 6
>
> "An operator with a service badge can open any compartment." — Section 8

A service operator is both allowed and forbidden to open the same occupied compartment. The keypad
authenticates knowledge of six digits. Recipient identity remains unchecked, so a delegated or guessed
code violates the sentence as written. Implementations can choose incompatible policies while each
claims to follow the spec.

Replace the identity claim with an explicit credential policy: an active pickup code or a valid
service badge may open the compartment. Add attempt throttling and state what an operator opening
does to the parcel, code, event log, and recipient notification.

`defect · direct-contradiction (contradiction)`

## Remaining finding index

- F4 · defect · The daily sweep enforces the 72-hour promise between hour 72 and hour 96 · Sections 6–7.
- F5 · defect · Notification retries end without a terminal failure action or operator signal · Sections 9–10.
- F6 · defect · Offline operation names no owner for code generation or conflict reconciliation · Sections 5 and 12.
- F7 · defect · `Registered` has no age-out path when a manifested parcel never arrives · Section 4.
- F8 · defect · Pickup and expiry can act on one parcel concurrently with no winner · Sections 6–7.
- F9 · defect · The event-log rule names writes but no reader, retention, or acting identity · Section 9.
- F10 · recommendation · Rewrite the deposit paragraph as ordered steps after its semantics are fixed · Section 5.

## Questions only the owner can answer

1. Who physically returns an expired parcel: Cedarline's operator or the carrier?
2. Is the pickup code intentionally a bearer credential, or must pickup prove recipient identity?
3. Must deposit work offline, or may an offline bank accept pickup and servicing only?

This pass left the reviewed document unchanged. The record contains the complete findings, coverage tables,
class sweep, assumptions, and ledger.
