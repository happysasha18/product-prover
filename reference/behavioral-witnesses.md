# Behavioral witnesses — conditional support for Phase 3

Open this file only when a suspected gap concerns repeated or overlapping operations, competing
conditional rules, a promise crossing a named component boundary, or eventual completion of a
repeated process. Use the smallest matching witness below to decide whether the concern is real.

These witnesses support the existing property analysis and stress lenses. They add no mandatory
surface sweep, no category tag, and no minimum finding count. A second method applied to the same
repair does not create a second finding.

## Rules shared by every witness

- Start from an operation, rule, boundary, or progress promise the document actually states.
- Name the source clauses and the precise obligation in dispute.
- Separate stated facts, reviewer assumptions, and proposed repairs. A proposed repair is not
  evidence about the current document.
- Record the initial conditions, actions or inputs, observable result, and the clause violated or
  left unanswered.
- Use the smallest witness that decides the concern. Do not enumerate a full state space when two
  steps or three rows are enough.
- If the document does not determine a step, mark that step **unspecified**. Do not present an
  invented execution as an established defect.
- Merge the witness into an existing finding when both point to the same repair.

## Replay or order witness

Arm this witness when the document names a repeated operation, a retry, replay or delivery, or two
operations over the same entity whose order may matter.

Choose one comparison:

1. Run one logical request once, then replay that same logical request. Compare state and every
   external effect, not only the final row in storage.
2. Run `A` then `B`, and compare it with `B` then `A`, where both orders are reachable.
3. For overlap, show one meaningful interleaving and the observation available to each actor.

File a finding only when the stated promise requires the two results to agree, or when the document
leaves a reachable order without an answer. Idempotence and commutativity are not universal
requirements: a document may deliberately reject a replay or prescribe an order. A physical action
need not have an inverse. Ask for monotonic behaviour only where the document promises it, and for
compensation only where it names cancellation or reversal.

## Rule-selection witness

Arm this witness when two or more stated conditions select one outcome, or when the document claims
that a set of rules forms a complete partition.

Build a small local table containing only the conditions needed to expose the concern:

| Reachable input | Applicable rules | Selected result |
|---|---|---|
| `<small case>` | `<none, one, or several>` | `<stated, conflicting, or unspecified>` |

Apply stated priority, defaults, exclusions, and exceptions before judging the table. A witness is a
hit when one reachable input has no applicable result despite a completeness promise, or has several
incompatible results with no precedence rule. Do not construct the full Cartesian product. Do not
turn an impossible combination into a gap. Label any inferred reachability condition as an
assumption.

## Boundary-promise witness

Arm this witness when a consumer relies on a named provider or component result.

Record four lines:

- Consumer requires: the fact needed for its next step.
- Provider guarantees: the strongest result the document actually promises.
- Conditions and timing: when that guarantee holds, including failure and timeout cases.
- Observable acknowledgement: what the consumer can distinguish.

A hit exists when a provider-permitted outcome is insufficient for the consumer's stated promise.
For example, acceptance into a queue does not establish receipt by a person. If the provider
contract is absent, report an unverified premise at the seam, not a proven provider violation.
Where components rely on one another cyclically, name the actor or event that supplies the first
trigger; do not assume the cycle starts itself.

## Progress witness

Arm this witness when the document promises eventual completion, a deadline, retry, or exit from a
queue or repeated process.

Record:

1. The state from which progress is promised.
2. The actor, timer, scheduler, or event that initiates the next step.
3. The condition that enables that step.
4. The shortest reachable cycle that repeats without reaching the promised result, if one exists.
5. The stated bound, retry limit, recovery path, or decreasing progress measure that breaks the
   cycle.

An available exit edge does not guarantee that anything will take it. A retry limit guarantees
termination, not success. A decreasing ranking measure is useful for a finite algorithm, but it is
not a universal requirement for a long-running service; a named scheduler, fairness assumption,
deadline, or recovery owner may be the correct evidence instead.

## Reporting

The witness belongs inside the ordinary four-part finding. Keep the sequence or table as short
evidence in Part 3, then use an existing plain-label and formal-term category. If the witness is
clean, it produces no finding and no separate verdict line. In the persisted record, include this
file's digest only when a witness from it was armed.
