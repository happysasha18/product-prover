# Parcel locker deposit

## Purpose

The service lets a courier leave a parcel in a self-service locker and lets the recipient collect it later with a pickup code.

## Actors and surfaces

- Courier — uses a handheld scanner to deposit a parcel.
- Locker controller — opens and closes a compartment, then records the parcel status.
- Notification service — sends the pickup code by SMS.
- Recipient — enters a pickup code at the locker.
- Nightly sweep — checks overdue parcels once each night.

## Deposit

1. The courier scans the parcel and selects an empty compartment.
2. The locker opens the compartment. The courier places the parcel inside and closes the door.
3. The locker controller marks the parcel `Stored`.
4. The system generates a pickup code and sends the code to the recipient by SMS.

The recipient has 72 hours to collect a stored parcel.

## Collection

The recipient enters the pickup code at the locker. If the code is valid, the locker opens the compartment and the recipient takes the parcel.

## Expiry

The nightly sweep marks a stored parcel `Expired` when its collection window has elapsed.
