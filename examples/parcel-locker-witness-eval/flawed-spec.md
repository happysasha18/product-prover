# Parcel locker witness fixture — flawed

This fictional fixture exists to test Product Prover's conditional behavioral witnesses.

## Model and promises

A parcel moves through `DepositPending`, `Stored`, `Collected`, `Expired`, and `Returned`. A
compartment holds at most one parcel. A recipient must receive one usable pickup code for a stored
parcel. The pickup code is valid for exactly 72 hours from `stored_at`. Every accepted deposit
eventually becomes `Stored` or returns to the carrier. Every notification in `DeliveryPending`
eventually becomes `Delivered` or `DeliveryFailed`. Retries of one logical deposit must return the
same pickup credential and enqueue only one notification.

## Deposit API

`POST /deposits` accepts `parcel_id`, `compartment_id`, and `request_id`. Network retries may repeat
the same logical request with the same `request_id`. Every accepted call generates a new six-digit
pickup code, stores it as active for the parcel, and enqueues an SMS. Exactly one pickup code is
active for a parcel at a time. The response is `202 Accepted`.

## Notification boundary

The notification gateway returns `Accepted` once it has queued an SMS. The locker service then marks
the recipient `Notified`; `Notified` means that the recipient has received the pickup code.

If delivery returns `TemporaryFailure`, the notification stays `DeliveryPending` and the same send
operation is retried until it returns `Delivered`. No retry owner, timer, limit, or terminal recovery
action is specified.

## Collection and expiry

The collection endpoint accepts the active pickup code when the parcel is `Stored` and
`now <= expires_at`; it opens the compartment and then marks the parcel `Collected`.

The expiry worker selects a `Stored` parcel when `now >= expires_at`, marks it `Expired`, and assigns
it to the return queue. Collection and expiry may run concurrently. They do not share a lock or
compare a version, and no precedence rule is specified.

The rule table says:

- when `now <= expires_at`, the result is `Collect`;
- when `now >= expires_at`, the result is `Expire`;
- otherwise, reject the request.
