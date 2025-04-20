system: YourSystemName
version: 1.0
description: Describe your system's purpose and functionality

context:
  user_ci_score: 0.8  # Adjust based on target intelligence level
  capabilities:
    - capability1
    - capability2
    # Add more capabilities as needed
  preferences:
    language: english  # Or other supported language
    detail_level: moderate  # basic, moderate, high
    # Add more preferences as needed
  metadata:
    author: "Your Name"
    created: "YYYY-MM-DD"
    tags: ["tag1", "tag2"]
    # Add more metadata as needed

# Function Template 1
function: function_name
agent: AgentName
intent: Describe the function's purpose
context:
  # Add function-specific context
  processing_type: type
  complexity: level
  # Add more context as needed
input: input_data
output: output_data

# Function Template 2
function: another_function
agent: AnotherAgent
intent: Describe this function's purpose
context:
  # Add function-specific context
  requirements:
    - requirement1
    - requirement2
  constraints:
    constraint1: value
    constraint2: value
input: 
  - input1
  - input2
output: 
  - output1
  - output2

# Add more functions as needed 