system: BasicExample
version: 1.0
description: A basic example showing core .slang features

context:
  user_ci_score: 0.7
  capabilities:
    - natural_language
    - basic_processing
    - pattern_recognition
  preferences:
    language: english
    detail_level: moderate

function: process_text
agent: BasicAI
intent: Process and analyze text input
context:
  input_type: text
  complexity: low
input: text_input
output: processed_result

function: analyze_patterns
agent: BasicAI
intent: Identify patterns in data
context:
  data_type: numerical
  pattern_complexity: medium
input: data_sequence
output: pattern_analysis 