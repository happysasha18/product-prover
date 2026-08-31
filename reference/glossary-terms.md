# Glossary terms — exact definitions for glossary mode

`SKILL.md`'s glossary mode opens this file before answering a glossary request. Use these
definitions exact, and paraphrase none of them loosely.

- **state-space** — the set of all situations the system can be in.
- **transitions** — the moves between states.
- **actors** — who initiates an action: user, role, automated service, external system.
- **composition** — how separate components combine. Clean when components have sharp roles.
- **abstraction** — replacing case-by-case enumeration with a general rule.
- **invariant** — a property that must hold across every reachable state.
- **precondition** — what must be true before an action runs.
- **postcondition** — what must be true after an action completes.
- **atomicity** — an operation either completes fully or leaves no trace.
- **rollback** — what the system reverts to on failure.
- **safety** — the family of properties meaning "nothing bad ever happens".
- **liveness** — the family of properties meaning "something good eventually happens".
- **dead-end** — a state with no defined exit.
- **discharge** — actually proving (or implementing) a property using the system's primitives.
- **consistency** — whether the spec's stated rules can all simultaneously hold.
- **contradiction** — two stated rules that openly conflict.
- **observability** — whether operators can see and understand the system's state.
- **cognitive-load** — mental effort users spend tracking modes, exceptions.
- **ops-ux** — operational UX: debuggability, audit trails, traceability.
