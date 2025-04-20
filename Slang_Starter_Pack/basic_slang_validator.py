class BasicSlangValidator:
    """A validator for .slang files with CI level awareness."""
    
    def __init__(self, ci_level: float = 0.5):
        """Initialize with optional CI level (0.0 to 1.0)."""
        self.ci_level = max(0.0, min(1.0, ci_level))
        self.required_sections = ['system', 'version']
        self.required_function_parts = ['input', 'output', 'agent', 'intent']
        self.errors = []
        self.warnings = []
        self.signals = []
        self.ci_insights = []
        
    def _record_signal(self, signal_type: str, message: str, ci_threshold: float = 0.0):
        """Record a signal if CI level is sufficient."""
        if self.ci_level >= ci_threshold:
            self.signals.append(f"{signal_type}: {message}")
            
    def _record_insight(self, insight: str, ci_threshold: float = 0.0):
        """Record an insight if CI level is sufficient."""
        if self.ci_level >= ci_threshold:
            self.ci_insights.append(insight)
        
    def validate(self, file_path: str) -> bool:
        """Validate a .slang file with CI-aware rules."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            # Remove empty lines and comments
            lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
            
            if not lines:
                self.errors.append("File is empty")
                return False
                
            # Check basic structure (always required)
            has_system = False
            has_version = False
            has_function = False
            system_name = ""
            context_found = False
            user_ci_score = 0.5  # Default if not specified
            
            for line in lines:
                if line.startswith('system:'):
                    has_system = True
                    system_name = line.split(':', 1)[1].strip()
                    self._record_signal("SYSTEM", f"Found system: {system_name}")
                elif line.startswith('version:'):
                    has_version = True
                    version = line.split(':', 1)[1].strip()
                    self._record_signal("VERSION", f"Found version: {version}")
                elif line == 'context:':
                    context_found = True
                    self._record_signal("CONTEXT", "Found context section", 0.3)
                elif context_found and line.startswith('  user_ci_score:'):
                    try:
                        user_ci_score = float(line.split(':', 1)[1].strip())
                        self._record_signal("CI", f"User CI score: {user_ci_score}", 0.3)
                    except ValueError:
                        self.warnings.append("Invalid user_ci_score format")
                elif line.startswith('function:'):
                    has_function = True
                    
            # Basic validation (always required)
            if not has_system:
                self.errors.append("Missing system name")
            if not has_version:
                self.errors.append("Missing version")
            if not has_function:
                self.errors.append("No functions defined")
                
            # CI-aware validation
            if self.ci_level >= 0.3:
                if not context_found:
                    self.warnings.append("No context section found")
                if user_ci_score < self.ci_level:
                    self._record_insight("System might be too complex for user's CI level", 0.3)
                
            # Check function structure
            current_function = None
            function_parts = set()
            function_complexity = {}
            
            for line in lines:
                if line.startswith('function:'):
                    # Check previous function if exists
                    if current_function and function_parts:
                        missing = set(self.required_function_parts) - function_parts
                        if missing:
                            self.errors.append(f"Function '{current_function}' missing: {', '.join(missing)}")
                        if self.ci_level >= 0.4:
                            complexity = len(function_parts) / len(self.required_function_parts)
                            function_complexity[current_function] = complexity
                            if complexity < 0.5:
                                self._record_insight(f"Function '{current_function}' might be too simple", 0.4)
                    
                    current_function = line.split(':', 1)[1].strip()
                    function_parts = set()
                    self._record_signal("FUNCTION", f"Checking function: {current_function}", 0.2)
                    
                    # Check if function has a valid name
                    if not current_function:
                        self.errors.append(f"Empty function name")
                    elif not current_function.isidentifier():
                        self.warnings.append(f"Function name '{current_function}' might not be a valid identifier")
                
                elif current_function and line.startswith('  '):
                    # Inside a function definition
                    line_lower = line.lower().strip()
                    for part in self.required_function_parts:
                        if line_lower.startswith(f"{part}:"):
                            function_parts.add(part)
                            value = line.split(':', 1)[1].strip()
                            if not value:
                                self.warnings.append(f"Empty {part} in function '{current_function}'")
                            self._record_signal("DETAIL", f"Function '{current_function}' {part}: {value}", 0.2)
                            
                            # CI-aware content analysis
                            if self.ci_level >= 0.5:
                                if part == 'complexity' and value in ['high', 'medium', 'low']:
                                    self._record_insight(f"Function '{current_function}' complexity: {value}", 0.5)
            
            # Check last function
            if current_function and function_parts:
                missing = set(self.required_function_parts) - function_parts
                if missing:
                    self.errors.append(f"Function '{current_function}' missing: {', '.join(missing)}")
            
            # CI-aware summary
            if self.ci_level >= 0.6:
                total_complexity = sum(function_complexity.values()) / len(function_complexity) if function_complexity else 0
                self._record_insight(f"Average function complexity: {total_complexity:.2f}", 0.6)
                if total_complexity > user_ci_score:
                    self._record_insight("System complexity exceeds user's CI level", 0.6)
            
            success = len(self.errors) == 0
            self._record_signal("RESULT", "Validation successful" if success else "Validation failed")
            return success
            
        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            return False
            
    def get_errors(self) -> list:
        """Get the list of validation errors."""
        return self.errors
        
    def get_warnings(self) -> list:
        """Get the list of validation warnings."""
        return self.warnings
        
    def get_signals(self) -> list:
        """Get the list of recorded signals."""
        return self.signals
        
    def get_insights(self) -> list:
        """Get the list of CI-aware insights."""
        return self.ci_insights

def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate .slang files with CI awareness')
    parser.add_argument('file', help='.slang file to validate')
    parser.add_argument('--ci', type=float, default=0.5, help='CI level (0.0 to 1.0)')
    args = parser.parse_args()
    
    validator = BasicSlangValidator(ci_level=args.ci)
    file_path = args.file
    
    print(f"\nChecking {file_path} (CI Level: {args.ci})...")
    if validator.validate(file_path):
        print("✓ File looks good!")
        print("\nStructure:")
        print("- Has system name")
        print("- Has version")
        print("- Has functions")
        
        if validator.get_warnings():
            print("\nSuggestions:")
            for warning in validator.get_warnings():
                print(f"  ! {warning}")
                
        if validator.get_signals():
            print("\nSignals:")
            for signal in validator.get_signals():
                print(f"  > {signal}")
                
        if validator.get_insights():
            print("\nInsights:")
            for insight in validator.get_insights():
                print(f"  * {insight}")
    else:
        print("✗ Found some issues:")
        for error in validator.get_errors():
            print(f"  - {error}")
        
        if validator.get_warnings():
            print("\nAlso noticed:")
            for warning in validator.get_warnings():
                print(f"  ! {warning}")
                
        if validator.get_signals():
            print("\nSignals:")
            for signal in validator.get_signals():
                print(f"  > {signal}")

if __name__ == "__main__":
    main() 