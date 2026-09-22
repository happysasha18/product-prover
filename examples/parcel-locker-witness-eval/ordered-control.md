# Explicitly ordered operations — negative control

This fictional payment protocol deliberately defines operations that do not commute.

An authorization begins in `Authorized`. `Capture` may run only from `Authorized` and changes the
payment to `Captured`. `Void` may run only from `Authorized` and changes it to `Voided`. A capture
after void and a void after capture both return `409` with the current terminal state. This order
dependence is intentional and part of the public contract.

Every command requires a stable `command_id`. Replaying a command returns its stored result without
calling the processor again. Two different commands race through one compare-and-set on the payment
version, so exactly one terminal transition wins. No rule promises that `Capture; Void` and
`Void; Capture` produce the same result.
