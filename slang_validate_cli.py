"""
slang_validate_cli.py: Validate .slang files for correct structure and required fields.
"""
import argparse
import sys
import json
from slang_parser import SlangParser

REQUIRED_FUNCTION_FIELDS = ["name", "agent", "intent", "input", "output"]

def validate_slang_file(path: str, schema_path: str = None) -> bool:
    """Parse and validate a .slang file. Optionally validate function contexts against a JSON schema."""
    try:
        content = open(path, 'r').read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    parser = SlangParser()
    try:
        parsed = parser.parse(content)
    except Exception as e:
        print(f"Parsing error: {e}")
        return False

    errors = []
    # Check system
    system = parsed.get('system', {})
    if not system.get('name'):
        errors.append("Missing system name.")

    # Check functions
    functions = parsed.get('functions', [])
    if not functions:
        errors.append("No functions defined.")
    else:
        for idx, fn in enumerate(functions, start=1):
            for field in REQUIRED_FUNCTION_FIELDS:
                if field not in fn or fn.get(field) in (None, ''):
                    errors.append(f"Function #{idx} missing '{field}'.")

    # If structural errors exist, report and exit
    if errors:
        print("Validation failed with the following errors:")
        for err in errors:
            print(f"  - {err}")
        return False

    print("Validation successful: .slang file is structurally sound.")
    # If schema validation requested, apply to each function context
    if schema_path:
        try:
            from jsonschema import validate, ValidationError
        except ImportError:
            print("jsonschema library is required for schema validation.")
            return False
        try:
            schema = json.load(open(schema_path))
        except Exception as e:
            print(f"Error loading schema: {e}")
            return False
        schema_errors = []
        for fn in parsed.get('functions', []):
            try:
                validate(instance=fn.get('context', {}), schema=schema)
            except ValidationError as e:
                schema_errors.append(f"Function '{fn.get('name')}' context schema error: {e.message}")
        if schema_errors:
            print("Schema validation failed:")
            for err in schema_errors:
                print(f"  - {err}")
            return False
        print(f"Schema validation successful against {schema_path}.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Validate a .slang file for correct structure.")
    parser.add_argument("file", help="Path to the .slang file to validate")
    parser.add_argument("--schema", help="Path to JSON schema for function contexts")
    args = parser.parse_args()

    ok = validate_slang_file(args.file, args.schema)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()