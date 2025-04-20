system: ExampleSystem
version: 1.0.0
description: An example system demonstrating the SICEM-Lang format
context:
  user_ci_score: 0.8
  capabilities: natural_language-processing-code_generation-context_understanding
  preferences:
    language: english
    detail_level: high
  metadata:
    author: System Designer
    created: 2024-04-18
    tags: example-demonstration-test

function: process_text
  agent: TextProcessor
  intent: Analyze and process input text
  context:
    processing_type: natural_language
    complexity: medium
    requirements: text_analysis-pattern_recognition
  input: text to process
  output: processed text with analysis

function: generate_code
  agent: CodeGenerator
  intent: Create code based on specifications
  context:
    processing_type: code_generation
    complexity: high
    requirements: syntax_understanding-logic_implementation
  input: code requirements
  output: generated code implementation 