
# System: CaitalystStrategySim.slang
# Simulation: Executive Strategy Session – Global Expansion 2026

system: CaitalystStrategySim
context:
  mode: executive_simulation
  focus: global_market_expansion
  user_role: strategic_observer

modules:
  - initiate_session
  - live_discussion_capture
  - inject_insight
  - decision_pivot
  - value_accumulation
  - wrap_transition
  - echo_summary_output

---

function: initiate_session
agent: Fai
intent: open_strategy_session
context:
  agenda: "Expansion risk and readiness"
  regions: ["LATAM", "Europe", "Southeast Asia"]
input: "Fai, start Global Expansion session."
output:
  prompt: "What key concerns exist when expanding into multiple markets?"
  trigger_agent: Train

---

function: live_discussion_capture
agent: Train
intent: transcribe_and_tag
input:
  discussion:
    - COO: "Operational maturity varies across regions."
    - Director: "If we launch LATAM and Europe together, risk spreads."
output:
  tags: ["Operational Readiness", "Launch Risk"]
  forward_to: Crit

---

function: inject_insight
agent: Crit
intent: analyze_tags_and_enrich
input: tags from Train
output:
  insight: "Pulls product performance data, suggests follow-up."
  follow_up_question: "How should we support LATAM vs. Europe?"

---

function: decision_pivot
agent: VP_Intl
intent: compare_localization
input:
  crit_question: "How do we localize support for LATAM vs Europe?"
output:
  option_a: "LATAM localized in Mexico and Brazil"
  option_b: "Europe more fragmented and expensive"
  recommendation: "Staggered entry — LATAM first"

---

function: value_accumulation
agent: Crit
intent: capture_risk_questions
input:
  ceo_request: "How can we avoid first-mover disadvantage in LATAM?"
output:
  questions_for_further_analysis:
    - "Ask about competitor advantage loss"
    - "Ask about risk mitigation scenarios"

---

function: wrap_transition
agent: Fai
intent: flag_decisions
input:
  final_discussion_summary: "Two pivots, three flagged risks"
output:
  forward_to: Echo
  final_query: "Logged. Forwarding to finance AI."

---

function: echo_summary_output
agent: Echo
intent: compile_session_output
input: logs from Train, flags from Fai, insights from Crit
output:
  transcript: full
  decision_summary: "LATAM prioritized, Q1 2026"
  actions: ["Financial modeling", "Localization readiness"]
  deliver_to: ExecInbox
