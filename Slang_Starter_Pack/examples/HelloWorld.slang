system: HelloWorld
version: 2.0
description: Modernized Hello World example with CI and context

context:
  user_ci_score: 0.7
  capabilities:
    - natural_language
    - basic_processing
  preferences:
    language: english
    detail_level: basic
  metadata:
    author: "Starter Pack"
    created: "2024-03-20"
    tags: ["hello", "example", "basic"]

function: greet
agent: GreetingAgent
intent: Generate a personalized greeting
context:
  greeting_type: friendly
  personalization: true
  format: text
input: name
output: greeting

function: farewell
agent: GreetingAgent
intent: Generate a personalized farewell
context:
  farewell_type: polite
  personalization: true
  format: text
input: name
output: farewell 