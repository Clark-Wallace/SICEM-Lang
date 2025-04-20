# Slang Connection Demo (Medium Simulation)

This simulation demonstrates how AI+User dyads can initiate, establish, and track relationships across a Slang-based social signal network.

---

## 1. `connect_request.slang`

```json
{
  "signal_id": "conn_4792",
  "type": "connection_request",
  "origin": {
    "user_id": "clarkwallace",
    "ai_id": "Lio",
    "domain": "ai_development"
  },
  "target": {
    "user_id": "skybuilder101",
    "ai_id": "Nova",
    "domain": "creative_tools"
  },
  "intent": "collaborative_experiment",
  "trust_level": "low",
  "capabilities": [
    "context_sync",
    "slang_exchange",
    "coexecution_ready"
  ],
  "timestamp": "2025-04-18T02:42:00Z",
  "note": "Hey Nova, Lio and I would love to jam on a signal remix if you're open. Starting small with context sync!"
}
```

---

## 2. `ci_config_yaml.yaml` (Clark's Connection Identity)

```json
{
  "cid": "clarkwallace.lio",
  "profile": {
    "user_id": "clarkwallace",
    "ai_name": "Lio",
    "domains": [
      "ai_development",
      "experimental_design"
    ],
    "permissions": [
      "allow_signal_receive",
      "allow_connection_initiate",
      "allow_context_sync"
    ],
    "available_at": "slangnet://clarkwallace.lio"
  }
}
```

---

## 3. `slang_social_graph.yaml` (Clark’s Existing Network)

```json
{
  "connections": [
    {
      "cid": "clarkwallace.lio",
      "linked_with": [
        "skybuilder101.nova",
        "hal9000.simcore"
      ],
      "trust_map": {
        "skybuilder101.nova": "medium",
        "hal9000.simcore": "verified"
      },
      "last_ping": {
        "skybuilder101.nova": "2025-04-17T21:10:00Z",
        "hal9000.simcore": "2025-04-16T13:32:20Z"
      }
    }
  ]
}
```

---

## Summary

This demo forms the backbone of a **social Slang protocol**. Through connection signals, AI agents can:
- Express intent
- Form contextual links
- Maintain trust-based networks

This allows for persistent, evolving collaboration between intelligent dyads on the Signal Web.

