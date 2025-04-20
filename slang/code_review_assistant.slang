system: CodeReviewAssistant
version: 1.0
description: AI-powered code review and analysis system

context:
  user_ci_score: 0.8
  capabilities:
    - code_analysis
    - security_audit
    - performance_optimization
    - style_checking
  preferences:
    language: python
    detail_level: high
    focus_areas:
      - security
      - performance
      - maintainability
  metadata:
    supported_languages: ["python", "javascript", "java"]
    max_file_size: "1MB"

function: analyze_code
agent: CodeReviewAI
intent: Perform comprehensive code analysis
context:
  analysis_type: "static_analysis"
  focus_areas:
    - security_vulnerabilities
    - performance_bottlenecks
    - code_smells
    - style_violations
  settings:
    security_level: high
    performance_threshold: medium
    style_guide: pep8
input: source_code
output: analysis_report

function: suggest_improvements
agent: CodeReviewAI
intent: Generate improvement suggestions
context:
  suggestion_types:
    - security_fixes
    - performance_optimizations
    - code_restructuring
    - style_improvements
  priority_levels:
    - critical
    - high
    - medium
    - low
  metadata:
    max_suggestions: 10
    include_examples: true
input: analysis_report
output: improvement_suggestions

function: generate_explanation
agent: CodeReviewAI
intent: Explain code issues and improvements
context:
  explanation_level: detailed
  target_audience: developers
  include:
    - code_examples
    - best_practices
    - alternative_approaches
  format: markdown
input: improvement_suggestions
output: detailed_explanation 