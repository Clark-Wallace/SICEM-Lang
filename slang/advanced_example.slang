system: AdvancedSystem
version: 2.0
description: Advanced example showing complex .slang features

context:
  user_ci_score: 0.9
  capabilities:
    - natural_language
    - code_generation
    - context_understanding
    - complex_analysis
  preferences:
    language: english
    detail_level: high
    response_format: detailed
  metadata:
    last_updated: "2024-03-20"
    author: "System Designer"
    tags: ["advanced", "example", "complex"]

function: complex_analysis
agent: GPT-4
intent: Perform complex multi-step analysis
context:
  analysis_type: "multi-dimensional"
  complexity: high
  requirements:
    - data_validation
    - pattern_recognition
    - trend_analysis
  constraints:
    max_processing_time: "5s"
    memory_limit: "1GB"
input: 
  - raw_data
  - analysis_parameters
output: 
  - analysis_results
  - confidence_scores
  - recommendations

function: content_adaptation
agent: GPT-4
intent: Adapt content for different intelligence levels
context:
  source_ci: 0.9
  target_ci: 0.6
  adaptation_rules:
    - simplify_complex_concepts
    - add_explanations
    - adjust_technical_depth
  metadata:
    supported_formats: ["text", "code", "diagrams"]
    max_content_length: 10000
input: original_content
output: adapted_content 