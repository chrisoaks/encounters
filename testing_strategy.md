## Testing strategy
- This application was written using TDD.  
- I wrote one test at a time and then made the minimum change required to get the test to pass.

### What I Tested
- Encounters can be created, and the endpoint returns the created encounter with generated id
- Encounters can be retrieved, and the endpoint returns 404 when not found
- Audit events are initially empty, but reveal reads and writes if/when they have occurred
- Audit events are filterable by start date and end date, both of which are optional
- Logs are scrubbed, as desired
- Views of the encounter audit require authentication
### Why these tests are critical
- These tests cover the basic requirements and support speed and confidence when refactoring

### How I made this testable
- Patching strategy was necessary only for inspecting logs, for this I used caplog
- If this application included more effects such as database writes:
  - I would have injected an in-memory repository during the fixture for app initialization in `conftest.py`
- 

### What I'd test with more time
- Test more logging behavior and try to find ways to break assumptions about the secret fields
- For example, test stringifying the objects and various calls to json.dumps or model_dumps_json
- Tests for generation of timestamps
- The writeup asks for an understanding of unit vs integration vs e2e testing.
  - The tests currently written are api-layer.  
  - This is to minimize internal coupling while still verifying required behavior.
  - More focused inspection of the log scrubbing could be done at the single-component level.


Coverage report as of ccbaa0bfd90cd48f2792d34a630d25e721a6e199:

Name                            Stmts   Miss  Cover
---------------------------------------------------
encounter_api/__init__.py           1      0   100%
encounter_api/dependencies.py      11      0   100%
encounter_api/encounters.py        85      0   100%
encounter_api/enums.py              5      0   100%
encounter_api/fastapi_app.py        8      0   100%
encounter_api/repository.py        23      0   100%
encounter_api/state.py             24      0   100%
encounter_api/types.py             45      3    93%
---------------------------------------------------
TOTAL                             202      3    99%