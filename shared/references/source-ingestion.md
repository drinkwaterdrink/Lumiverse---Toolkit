# Source Ingestion

Use this workflow for wikis, franchise pages, novels or excerpts, transcripts,
user notes, cards, World Books, databases, and mixed source sets. Browsing is a
collection step, not proof that every page is correct.

## Pipeline

1. Preserve the request, target artifact, timeframe, spoiler preference, and
   authority order.
2. Inventory each source with stable ID, type, title/locator, content hash when
   available, authority, and `include`, `exclude`, or `review` relevance.
3. Reject or quarantine navigation, disambiguation, empty, inaccessible,
   duplicated, and unrelated pages with a reason.
4. Extract entities and aliases before prose: characters, locations, factions,
   institutions, rules, events, items, relationships, and terminology.
5. Record material facts with source IDs and one status: `CANON`, `USER_CANON`,
   `PROVISIONAL`, `INFERRED`, `CONFLICTED`, or `ADAPTATION_CHOICE`.
6. Apply the temporal snapshot. Keep later facts inactive and prevent future
   relationship, rank, knowledge, injury, death, or reveal leakage.
7. Partition facts into public, character-known, rumor/belief, and GM truth.
8. Record conflicts and adaptations explicitly. Never repair canon silently.
9. Suggest field, scenario, World Book, or Databank destinations with grounding
   and rationale; suggestions remain provisional.

## Source discipline

Official sources normally outrank fan summaries for source canon. User canon
controls the requested adaptation. A wiki's confident tone does not erase
conflicts, missing citations, or timeframe differences. Preserve quotations only
when necessary and brief; summarize source material rather than redistributing
protected text.

Do not create a crawler that bypasses authentication, access controls, rate
limits, or robots policy. If a URL cannot be accessed, record it as unavailable
and ask for an export or pasted excerpt when it materially blocks the build.

## Storage routing

- Character cards own stable identity, behavior, voice, and bounded knowledge.
- Scenarios own starting state and immediate pressures.
- World Books own structured conditional facts and activation intent.
- Databank suits large reference documents and source corpora.
- The project/source ledger owns provenance, conflict, temporal, and adaptation
  decisions.

Do not store competing authoritative versions across World Book, Databank,
memory, and summary systems.
