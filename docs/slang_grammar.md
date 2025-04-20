# Slang File Grammar

Slang is a lightweight DSL for defining AI interactions, featuring a system declaration, context sections, and function blocks.

Basic structure:
```yaml
system: <SystemName>
context:
  <key>: <value>
  ...

function: <FunctionName>
agent: <AgentName>
intent: <IntentDescription>
context:
  <key>: <value>
input: <InputPlaceholder>
output: <OutputPlaceholder>
```

Rules:
- `system` appears once at the top and defines the interaction context.
- `context` sections are optional but may include metadata for AI adaptation.
- Each `function` block must include exactly one `function`, `agent`, `intent`, `input`, and `output`.
- Nested `context` under functions is YAML-indented key/value pairs.
- Blocks are separated by blank lines or by the start of the next `function:`.

Examples:
```yaml
system: Handshake

function: hang
agent: UserAI
intent: invite_to_session
context:
  session_id: "<uuid>"
input: N/A
output: session:<uuid>
```