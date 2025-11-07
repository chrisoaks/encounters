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

###
