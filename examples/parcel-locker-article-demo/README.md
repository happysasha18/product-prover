# Parcel-locker article demonstration

This folder preserves the controlled example used in the Medium article *Prose as Code: Applying
Formal Verification to Product Specs*.

- [`parcel-locker-spec.md`](parcel-locker-spec.md) is the exact deliberately incomplete input.
- [`review-2026-09-07.md`](review-2026-09-07.md) is the complete review produced in `FULL` mode by
  Product Prover v4.3.0 on 2026-09-07.

The source spec intentionally omits the recovery and completion rules that the review identifies.
Names such as `CodePending`, `Collected`, and `ReturnPending` occur first in the review's proposed
repairs; they are not hidden states in the source spec. The article shows a shortened selection of
the run. Read the full review for the remaining recovery and recipient-facing findings.

This is an explanatory historical artifact. It is not a production specification, a claim about a
real parcel-locker service, or the current release's canonical evaluation fixture. Its F4 infers
that the nightly sweep leaves codes usable beyond 72 hours; the source spec does not actually state
the collection guard, so Product Prover 1.7.0 reports that guard and the expiry race as unspecified
instead of asserting the inferred runtime behaviour. The historical review itself remains unchanged.
