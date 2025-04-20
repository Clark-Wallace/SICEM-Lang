
# System: SignalTrainerSystem.slang
# Purpose: Modular agent communication and contextual signal learning

modules:
  - simulate_dialogue_exchange
  - tag_ci_signalblock
  - evaluate_interaction_alignment
  - route_to_writer_or_trainer

---

function: simulate_dialogue_exchange
agent: DialogueSim
intent: generate_ci_signalblock
context:
  simulation_mode: general_dialogue
  tone_range: [neutral, smartallic, defiant]
input: "You said this was free, now you're asking for money."
output:
  signalblock:
    line: "You said this was free, now you're asking for money."
    tags:
      - ci_score: 0.4
      - logic_type: "promise contradiction"
      - tone: "accusatory"
      - humor: "situational irony"
      - interaction_alignment: "defiant"

---

function: tag_ci_signalblock
agent: Crit
intent: enrich_signal_tags
context:
  validation_mode: true
input:
  signalblock (from DialogueSim)
output:
  validation_status: confirmed
  pass_to: route_to_writer_or_trainer
