import json
import jsonschema
from pathlib import Path
from typing import Dict, Any, List, Optional

class SlangValidator:
    def __init__(self, schema_path: str = None):
        """Initialize the validator with the schema file."""
        if schema_path is None:
            # Get the directory where this script is located
            script_dir = Path(__file__).parent
            self.schema_path = script_dir / "slang_schema.json"
        else:
            self.schema_path = schema_path
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict[str, Any]:
        """Load the JSON schema from file."""
        with open(self.schema_path, 'r') as f:
            return json.load(f)
    
    def _parse_array(self, value: str, separator: str = '-') -> List[str]:
        """Parse a string into an array using the specified separator."""
        value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            # Handle array syntax [item1, item2, ...]
            value = value[1:-1]  # Remove brackets
            separator = ','
        return [item.strip() for item in value.split(separator)]
    
    def _parse_slang(self, content: str) -> Dict[str, Any]:
        """Parse a .slang file into a dictionary structure."""
        result = {
            "system": "",
            "version": "",
            "description": "",
            "context": {
                "user_ci_score": 0.0,
                "capabilities": [],
                "preferences": {},
                "metadata": {
                    "author": "",
                    "created": "",
                    "tags": []
                }
            },
            "functions": []
        }
        
        current_section = None
        current_function = None
        current_context = None
        indent_level = 0
        
        for line in content.split('\n'):
            line = line.rstrip()
            if not line:
                continue
                
            # Calculate indentation level
            current_indent = len(line) - len(line.lstrip())
            if current_indent > indent_level:
                indent_level = current_indent
                continue
            elif current_indent < indent_level:
                indent_level = current_indent
                if current_section == 'context':
                    current_context = None
            
            line = line.strip()
            
            if line.startswith('system:'):
                result["system"] = line.split(':', 1)[1].strip()
            elif line.startswith('version:'):
                result["version"] = line.split(':', 1)[1].strip()
            elif line.startswith('description:'):
                result["description"] = line.split(':', 1)[1].strip()
            elif line == 'context:':
                current_section = 'context'
            elif line.startswith('function:'):
                if current_function:
                    result["functions"].append(current_function)
                current_function = {
                    "name": line.split(':', 1)[1].strip(),
                    "agent": "",
                    "intent": "",
                    "context": {},
                    "input": "",
                    "output": ""
                }
                current_section = 'function'
            elif line.startswith('agent:'):
                if current_section == 'function':
                    current_function["agent"] = line.split(':', 1)[1].strip()
            elif line.startswith('intent:'):
                if current_section == 'function':
                    current_function["intent"] = line.split(':', 1)[1].strip()
            elif line.startswith('input:'):
                if current_section == 'function':
                    current_function["input"] = line.split(':', 1)[1].strip()
            elif line.startswith('output:'):
                if current_section == 'function':
                    current_function["output"] = line.split(':', 1)[1].strip()
            elif current_section == 'context':
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == 'user_ci_score':
                        result["context"]["user_ci_score"] = float(value)
                    elif key == 'capabilities':
                        result["context"]["capabilities"] = self._parse_array(value, '-')
                    elif key == 'preferences':
                        current_context = 'preferences'
                        result["context"]["preferences"] = {}
                    elif key == 'metadata':
                        current_context = 'metadata'
                    elif current_context:
                        if ':' in value:
                            subkey, subvalue = value.split(':', 1)
                            subkey = subkey.strip()
                            subvalue = subvalue.strip()
                            if current_context == 'metadata' and subkey == 'tags':
                                result["context"]["metadata"]["tags"] = self._parse_array(subvalue)
                            else:
                                result["context"][current_context][subkey] = subvalue
                        else:
                            result["context"][current_context][key] = value
            elif current_section == 'function' and line.startswith('  '):
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    if key.strip() == 'requirements':
                        current_function["context"][key.strip()] = self._parse_array(value.strip(), '-')
                    else:
                        current_function["context"][key.strip()] = value.strip()
        
        if current_function:
            result["functions"].append(current_function)
            
        return result
    
    def validate_file(self, file_path: str) -> List[str]:
        """Validate a .slang file against the schema."""
        errors = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            parsed = self._parse_slang(content)
            jsonschema.validate(instance=parsed, schema=self.schema)
            
        except jsonschema.exceptions.ValidationError as e:
            errors.append(f"Schema validation error: {str(e)}")
        except Exception as e:
            errors.append(f"Error parsing file: {str(e)}")
            
        return errors

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate .slang files')
    parser.add_argument('files', nargs='+', help='.slang files to validate')
    args = parser.parse_args()
    
    validator = SlangValidator()
    
    for file_path in args.files:
        print(f"\nValidating {file_path}...")
        errors = validator.validate_file(file_path)
        
        if errors:
            print("Validation failed:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("Validation passed!")

if __name__ == "__main__":
    main() 