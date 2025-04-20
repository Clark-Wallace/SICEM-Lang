# SICEM-Lang Examples

This directory contains example `.slang` files demonstrating different use cases and features of the SICEM-Lang system.

## File Structure

1. **Basic Examples**
   - `basic_example.slang` - Core features and basic structure
   - `micro_context_example.slang` - Focused, single-purpose systems
   - `template.slang` - Starter template for new projects

2. **Advanced Examples**
   - `advanced_example.slang` - Complex features and nested structures
   - `code_review_assistant.slang` - Real-world code review system
   - `multi_modal_processor.slang` - Multi-modal input/output handling

3. **Specialized Examples**
   - `data_analysis.slang` - Data processing and analysis
   - `content_generator.slang` - Content creation and adaptation
   - `system_integrator.slang` - System integration and orchestration

## Key Concepts

1. **System Definition**
   ```slang
   system: SystemName
   version: 1.0
   description: System description
   ```

2. **Context**
   ```slang
   context:
     user_ci_score: 0.8
     capabilities: [...]
     preferences: {...}
     metadata: {...}
   ```

3. **Functions**
   ```slang
   function: function_name
   agent: AgentName
   intent: Function purpose
   context: {...}
   input: input_data
   output: output_data
   ```

## Usage

1. Start with `template.slang` for new projects
2. Copy relevant sections from examples
3. Modify according to your needs
4. Use the Python tools to process and execute

## Best Practices

1. Keep context clear and focused
2. Use meaningful function names
3. Specify capabilities and preferences
4. Include relevant metadata
5. Document complex structures 