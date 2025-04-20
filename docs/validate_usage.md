# .slang Validation CLI

Use `slang_validate_cli.py` to verify that `.slang` files conform to the core grammar.

Usage:
```bash
# Validate a .slang file
python3 slang_validate_cli.py path/to/file.slang [--schema path/to/schema.json]

# Exit code 0 indicates success; any non-zero indicates validation errors.
```

Validation checks:
- Presence of a `system` name
- At least one `function` block defined
- Each function has `name`, `agent`, `intent`, `input`, and `output`
- (Optional) Validate function contexts against the provided JSON schema

Example:
```bash
$ python3 slang_validate_cli.py session_examples/yard_service_hang.slang
Validation successful: .slang file is structurally sound.
```