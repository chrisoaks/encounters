# Encounter API

## Setup & Running
```shell
uv venv
uv sync
uvicorn encounter_api.fastapi_app:create_app --factory --reload
```

## Design Decisions
- Key architectural choices
  - Obfuscation is implemented by deserializing sensitive information into fields with scrubbing repr and str functions.
    - Considered scrubbing at point of logging rather than at point of deserialization.
    - However, the present design makes it difficult to represent the sensitive data in any context, which feels safer.
  - There is some separation of concerns as api-interface layer is separate from the data model.
    - This introduces some duplication as most models have to be declared twice.
    - However, it forces more intentionality when changing the public interface.
  - Since python prefers snake_case, camelCase keys as requested by the documentation are converted at the api boundary.
- Alternatives considered
  - Considered modeling audit events separately from encounter data, but decided the requirements didn't warrant it.
  - list_audit_events_for_encounters is taking all the filtering responsibilities
    - An alternative design could shift this work to a service layer so that filtering could be tested independently

- Changes for production
  - Use a more robust approach to authentication
    - If continuing with API keys, the currently inline definitions would move to encrypted storage.
    - However, since this is probably a user-facing app, auth would likely be switched to asymmetric expiring JWT.
  - Add durability, encounters are currently stored in memory only.
    - We should introduce a database (e.g., postgres).
    - This can be done with minimal disruption given the decoupling of storage from the api via the repository pattern.
  - The audit view lacks indexing which will make sorting and filtering infeasible at some scale.
    - A production ready design might decouple the writes of the auditable events from the views.
      - This would support more complex query patterns not presently expected.
  - Increase usage of types and increase the mypy strictness.

## Testing philosophy
- Tests are designed to be fast and to demonstrate application behavior
- Tests are not designed to be airtight and are not intended to check behavior that can be caught statically.
- Generally prefer tests written at the api-layer to minimize the publicity of interfaces.
- Tests should continue to avoid database writes even after this application is shifted to use real persistence.
- Tests should avoid abstraction and allow some duplication in the name of increasing obviousness.
- How to run tests:
```shell
pytest tests
```