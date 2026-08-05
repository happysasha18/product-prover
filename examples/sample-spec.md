# Cedarline Lockers — parcel pickup, release 2 (sample spec)

*This document is fictional. Cedarline Lockers is an invented company and this spec describes no real
system. It ships with the product-prover skill as a practice document, and it holds gaps on purpose,
so a reader can run a review against it and compare what the review found with what they saw
themselves.*

---

## 1. Purpose

Cedarline operates banks of parcel lockers in supermarkets and transport hubs. A courier deposits a
parcel into a free compartment, the recipient gets a pickup code, and the recipient opens the
compartment with that code within the pickup window. Release 2 adds the pickup window and the expiry
sweep to the release 1 deposit flow.

## 2. Actors

- **Courier** — deposits parcels, and holds a courier badge scanned at the locker bank.
- **Recipient** — the person the parcel is addressed to.
- **Operator** — Cedarline staff who service a locker bank on site.
- **Notification service** — a third-party SMS gateway that delivers pickup codes.

## 3. Entities

- **Parcel** — one shipment, identified by a tracking number.
- **Compartment** — one lockable box in a bank. A compartment is free or occupied.
- **Pickup code** — a six-digit code tied to one parcel and one compartment.

## 4. Parcel states

1. **Registered** — the carrier has told Cedarline the parcel is coming. Entered when the carrier's
   manifest arrives.
2. **Stored** — the parcel sits in a compartment and the pickup window is running. Entered at
   deposit.
3. **PickedUp** — the recipient has opened the compartment and taken the parcel. Terminal.
4. **Expired** — the pickup window ran out with the parcel still in the compartment.

## 5. Deposit

The courier scans their badge, scans the parcel's tracking number, and the locker bank opens a free
compartment. The courier puts the parcel in and shuts the door. Cedarline then marks the parcel
Stored, generates a pickup code, and sends the code to the recipient by SMS.

A parcel whose tracking number is unknown to Cedarline is refused at the scan, and the bank opens no
compartment.

## 6. Pickup

The recipient types the six-digit code on the bank's keypad. The bank opens the compartment holding
that parcel. Closing the door marks the parcel PickedUp and the compartment free.

Only the recipient can open a compartment holding a parcel.

The pickup window is 72 hours from deposit.

## 7. Expiry

The expiry sweep runs daily at 03:00 and moves every parcel whose pickup window has run out into
Expired. An expired parcel is returned to the carrier.

## 8. Operator servicing

An operator with a service badge can open any compartment in a bank, so a jammed door, a parcel left
by mistake, and a cleaning round are all serviceable on site.

## 9. Stated rules

- Every parcel receives its pickup code within one minute of deposit.
- A compartment holds one parcel at a time.
- A pickup code opens one compartment and stops working once the parcel leaves it.
- Every deposit and every opening is written to the bank's event log.

## 10. Notification

Pickup codes go out over the SMS gateway. The gateway accepts a send request and reports delivery
asynchronously. Cedarline retries a failed send three times, at one minute, five minutes, and
fifteen minutes.

## 11. Reporting

The operations dashboard shows, per bank: compartments free, parcels stored, and parcels expired
today.

## 12. Non-functional

- A bank works while its network link is down, and it syncs events when the link returns.
- Keypad entry to door open takes under two seconds.

## 13. Open items

- **TBD:** what the courier does when a bank has no free compartment at deposit time.
- **Open question:** should a recipient be able to hand their code to someone else, and does the
  spec need to say anything about it?
- The refund path for a parcel damaged inside a compartment is out of scope for release 2.
