# Evidence Model

Use evidence labels to describe what is known, not how confident the writer
feels.

| Maturity | Meaning | Minimum evidence |
|---|---|---|
| `concept` | Useful design with no chosen serialization or runtime proof | A rationale; evidence may be empty |
| `static_validated` | Structure or content passed deterministic checks | Validator, schema, native template, or exact comparison |
| `simulated` | Expected behavior was exercised outside Lumiverse | Fixture and simulator/simulation record |
| `runtime_observed` | Behavior was observed in Lumiverse | `user_reported` or `captured_diagnostics`, plus the observed result |
| `certified_for_build` | Repeatable runtime evidence applies to a named build | Named Lumiverse build plus repeatable diagnostic evidence |

Never promote one level implicitly. A valid JSON file is not an import test; an
import is not an activation test; a simulated response is not model/runtime
evidence. Record the model, preset, provider, attachments, and build when they
materially affect an observation.

Every releasable connected package should include a capability receipt using
`lumiverse-toolkit.capability-receipt/v1`. List dependencies and limitations
even when empty. When evidence is user-reported, preserve that attribution.

## Mechanic maturity

Optional mechanics use the same ladder. A producer may emit only what its
declared maturity supports. A future consumer or extension does not make a
static artifact runtime-certified. When a producer and consumer mature at
different times, record both sides separately and specify graceful degradation.
