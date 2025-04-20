# Getting Started with SICEM-Lang

Welcome to SICEM-Lang! This guide will help you get started with creating and running your first .slang files.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/sicem-lang.git
   cd sicem-lang
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Your First .slang File

Create a new file named `MyFirstSystem.slang`:

```slang
system: MyFirstSystem
version: 1.0
description: My first SICEM-Lang system

context:
  user_ci_score: 0.7
  capabilities:
    - natural_language
    - basic_processing
  preferences:
    language: english
    detail_level: basic

function: process_input
agent: BasicProcessor
intent: Process user input
context:
  processing_type: simple
input: user_input
output: processed_result
```

## Running Your System

1. Use the slang runner:
   ```bash
   python slang_runner.py MyFirstSystem.slang
   ```

2. Or use the CLI:
   ```bash
   python slang_cli.py run MyFirstSystem.slang
   ```

## Key Concepts

1. **System Definition**
   - Every .slang file starts with a system definition
   - Includes version and description
   - Defines the overall purpose

2. **Context**
   - Specifies intelligence level (CI score)
   - Lists capabilities
   - Sets preferences
   - Includes metadata

3. **Functions**
   - Define specific operations
   - Specify input/output
   - Include context and intent

## Next Steps

1. **Explore Examples**
   - Check out the examples in the `examples/` directory
   - Try modifying them to understand how they work

2. **Create Your Own**
   - Start with simple systems
   - Gradually add complexity
   - Use the template as a reference

3. **Learn More**
   - Read the technical manual
   - Check out advanced examples
   - Join the community

## Common Patterns

1. **Basic System**
   ```slang
   system: BasicSystem
   context:
     user_ci_score: 0.7
     capabilities: [...]
   function: basic_function
     ...
   ```

2. **Advanced System**
   ```slang
   system: AdvancedSystem
   context:
     user_ci_score: 0.9
     capabilities: [...]
     metadata: {...}
   function: complex_function
     ...
   ```

## Getting Help

- Check the documentation
- Join our community
- Open an issue on GitHub