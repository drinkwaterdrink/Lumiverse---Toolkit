# Pressure Graph and Audit

## Build the graph

Represent each active situation node with:

```yaml
node_id: stable label
entry_conditions: what makes the node active
npc_goals: who wants what now
visible_signals: what can be noticed without forced success
concealed_information: fact plus current knowers
discovery_routes: observation, conversation, records, consequences, or inference
clock:
  advances_when: explicit conditions
  stages: escalating states
  consequences: world/NPC changes, never a forced user choice
state_effects: facts changed if this node resolves or advances
exits: possible next nodes
recombines_at: shared situation where different paths can meet
```

The user does not need to see full YAML. A compact table or bullets are usually more readable on mobile.

## Graph design rules

- Use at least two pressures that can advance independently.
- Give ordinary pressures enough weight to sustain play without the mystery.
- Give every secret two plausible discovery routes when practical.
- Advance clocks by conditions or time, not because the plot “needs” a twist.
- Let ignored threads change offscreen through NPC action.
- Include de-escalation, delay, redirection, and mundane-resolution paths.
- Recombine through shared spaces, resources, NPC needs, evidence, or consequences—not by forcing the user back to a main quest.
- Track state changes so resolved hooks do not reset silently.

## Continuity state

Track only what future scenes need:

- current time/date and active location;
- presence and availability;
- who knows/suspects each secret;
- active clock stages;
- promises, boundaries, debts, injuries, possessions, access, and resources;
- relationship changes actually earned in play;
- anomaly evidence and mundane explanations tested.

## Audit questions

1. Can the opening be played immediately?
2. Can the scenario move if `{{user}}` refuses the most obvious hook?
3. Do NPCs want different things and know different things?
4. Can secrets be discovered without guaranteed perception or exposition?
5. Are clocks conditional and their consequences reversible or redirectable where appropriate?
6. Does each expansion hook preserve the original opening and agency contract?
7. Is any provisional addition presented as approved canon?
8. Does the supernatural intensity match the requested tone?
9. Does the last line equal `Seed locked.` with nothing after it?

