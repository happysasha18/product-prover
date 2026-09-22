# Parcel locker witness fixture — repaired control

This fictional control resolves the witness-level gaps in `flawed-spec.md`.

## Model and promises

A parcel moves through `DepositPending`, `Stored`, `Collecting`, `Collected`, `Expired`,
`ReturnPending`, and `Returned`. A compartment holds at most one parcel. Exactly one pickup
credential is active for each `Stored` parcel. The credential is valid on the half-open interval
`stored_at <= now < expires_at`, where `expires_at = stored_at + 72 hours` on the locker's monotonic
server clock.

## Deposit API and replay

`POST /deposits` requires a stable `request_id`. The service stores the first result by
`request_id`. A replay with the same parcel and compartment returns that result without generating a
credential or notification. Reuse of the identifier with different inputs returns `409 Conflict`.
The parcel becomes `Stored` only after the compartment confirms door closure and the credential is
stored.

## Notification boundary and progress

The notification gateway's `Accepted` result means only that the SMS is queued. The locker service
records `Queued`, not `Delivered`, and tells the recipient-facing surface that delivery is pending.
A delivery receipt changes it to `Delivered`.

A scheduler owns retries and records `delivery_started_at` when a notification enters
`DeliveryPending`. It retries at 1, 6, and 35 minutes after that timestamp; each send attempt times
out after 30 seconds. The scheduler is required to start each attempt within five seconds of its
scheduled time. If no `Delivered` receipt has arrived by `delivery_started_at + 36 minutes`, the
scheduler atomically sets `DeliveryFailed`, alerts the bank operator, and exposes credential
reissue. Permanent failure may take that path earlier. A late receipt does not reopen a terminal
record. This deadline applies to queued messages and timed-out attempts alike.

## Collection and expiry

Collection and expiry use one atomic compare-and-set on the parcel version. Collection may claim
`Stored` as `Collecting` only while `now < expires_at`; only after that claim does it command the
door to open. Expiry may change `Stored` to `Expired` only while `now >= expires_at`. A losing
operation reloads and returns the winning state. Once `Collecting` is claimed, expiry ignores the
parcel and the opening may complete as `Collected` even if the clock crosses `expires_at`. If the
door fails to open, a 30-second recovery changes `Collecting` back to `Stored` when time remains or
to `Expired` otherwise. The two initial guards do not overlap, including at
`now == expires_at`.
