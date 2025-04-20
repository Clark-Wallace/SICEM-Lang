
---

function: interpret_user_intent
agent: IntentCatcher
intent: map_natural_language_to_action
input: "I want to automate renaming files"
output:
  task_type: automation
  concept_area: scripting
  abstraction_preference: medium
  context_style: modular_chunks

---

function: translate_to_task_blocks
agent: TaskMapper
intent: convert_to_steps
context:
  from: IntentCatcher
  user_mode: concept-guided
output:
  step_1: define_target_directory()
  step_2: loop_through_files()
  step_3: rename_files_with_pattern()
  offer_next: true

---

function: deliver_chunked_support
agent: Prosayer
intent: explain_task_blocks
input:
  block: rename_files_with_pattern()
output:
  chunked_explanation:
    - "This part walks through each file in the folder."
    - "It replaces the old name using a pattern you define."
    - "No files are deleted — it's just a name swap."
