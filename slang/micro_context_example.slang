system: MicroContextExample
version: 1.0
description: Example showing focused, single-purpose systems

# Example 1: Simple Text Processor
context:
  user_ci_score: 0.6
  capabilities:
    - text_processing
  preferences:
    language: english
    detail_level: basic

function: process_text
agent: TextProcessor
intent: Basic text processing
context:
  processing_type: simple
input: text_input
output: processed_text

# Example 2: Data Validator
context:
  user_ci_score: 0.7
  capabilities:
    - data_validation
  preferences:
    format: json
    strict_mode: true

function: validate_data
agent: DataValidator
intent: Validate data structure
context:
  validation_rules:
    - required_fields
    - type_checking
input: data_object
output: validation_result

# Example 3: Status Checker
context:
  user_ci_score: 0.5
  capabilities:
    - status_monitoring
  preferences:
    check_interval: "1m"
    alert_level: warning

function: check_status
agent: StatusMonitor
intent: Monitor system status
context:
  check_types:
    - system_health
    - resource_usage
input: system_metrics
output: status_report 