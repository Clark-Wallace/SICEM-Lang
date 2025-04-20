
# System: SignalProsayer.slang
# Purpose: A context-aware support engine that adapts code, logic, or concept delivery to user CI preferences

system: SignalProsayer
context:
  user_ci_score: dynamic
  explanation_mode: adaptive
  chunk_delivery: enabled

modules:
  - interpret_user_intent
  - translate_to_task_blocks
  - deliver_chunked_support
  - monitor_context_curiosity
  - log_signal_growth
