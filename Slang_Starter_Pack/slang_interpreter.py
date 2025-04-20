import re
import sys
from datetime import datetime

class SlangInterpreter:
    """A basic interpreter for .slang files with CI level awareness."""
    
    def __init__(self, ci_level: float = 0.5):
        """Initialize with optional CI level (0.0 to 1.0)."""
        self.ci_level = max(0.0, min(1.0, ci_level))
        self.functions = {}
        self.context = {}
        self.signals = []
        self.fridge = []
        self.reminders_enabled = True
        
    def _record_signal(self, signal_type: str, message: str, ci_threshold: float = 0.0):
        """Record a signal if CI level is sufficient."""
        if self.ci_level >= ci_threshold:
            self.signals.append(f"{signal_type}: {message}")
            
    def load_file(self, file_path: str) -> bool:
        """Load and parse a .slang file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            current_function = None
            current_section = None
            
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                if line.startswith('system:'):
                    self._record_signal("SYSTEM", f"Loading system: {line.split(':', 1)[1].strip()}")
                elif line.startswith('version:'):
                    self._record_signal("VERSION", f"Version: {line.split(':', 1)[1].strip()}")
                elif line == 'context:':
                    current_section = 'context'
                    self.context = {}
                elif line.startswith('function:'):
                    current_section = 'function'
                    current_function = line.split(':', 1)[1].strip()
                    self.functions[current_function] = {
                        'agent': '',
                        'intent': '',
                        'context': {},
                        'input': '',
                        'output': ''
                    }
                elif current_section == 'context' and ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'user_ci_score':
                        self.context['user_ci_score'] = float(value)
                    else:
                        self.context[key] = value
                elif current_section == 'function' and current_function:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in ['agent', 'intent', 'input', 'output']:
                            self.functions[current_function][key] = value
                        else:
                            self.functions[current_function]['context'][key] = value
                            
            self._record_signal("LOAD", f"Loaded {len(self.functions)} functions")
            return True
            
        except Exception as e:
            self._record_signal("ERROR", f"Error loading file: {str(e)}")
            return False
            
    def execute_function(self, function_name: str, input_data: str = None) -> str:
        """Execute a function with optional input."""
        if function_name not in self.functions:
            self._record_signal("ERROR", f"Function '{function_name}' not found")
            return None
            
        func = self.functions[function_name]
        
        # Basic execution (CI 0.0-0.3)
        if self.ci_level < 0.3:
            return f"Executed {function_name} with input: {input_data}"
            
        # Enhanced execution (CI 0.3-0.5)
        if self.ci_level >= 0.3:
            self._record_signal("EXEC", f"Executing {function_name} with agent: {func['agent']}")
            
        # Process input based on function context
        if input_data:
            if func['agent'] == 'TextProcessor':
                # Basic text processing
                processed = input_data.lower()
                if self.ci_level >= 0.5:
                    # Add more sophisticated processing
                    processed = processed.capitalize()
                    if 'pattern_recognition' in func['context'].get('requirements', ''):
                        # Count words and characters
                        word_count = len(processed.split())
                        char_count = len(processed)
                        processed = f"Processed text: {processed}\nWord count: {word_count}\nCharacter count: {char_count}"
                return processed
                
            elif func['agent'] == 'CodeGenerator':
                # Basic code generation
                if self.ci_level >= 0.5:
                    if 'syntax_understanding' in func['context'].get('requirements', ''):
                        # Generate a simple function based on input
                        return f"def generated_function():\n    # {input_data}\n    pass"
                return f"# Code generation placeholder for: {input_data}"
                
        # Context-aware execution (CI 0.5-0.7)
        if self.ci_level >= 0.5:
            if 'complexity' in func['context']:
                complexity = func['context']['complexity']
                if complexity == 'high' and self.ci_level < 0.7:
                    self._record_signal("WARNING", f"Function complexity ({complexity}) exceeds CI level", 0.5)
                    
        # Advanced execution (CI 0.7+)
        if self.ci_level >= 0.7:
            # Add more sophisticated processing here
            pass
            
        return func['output']
        
    def get_signals(self) -> list:
        """Get the list of recorded signals."""
        return self.signals

    def parse_temporal_contents(self):
        contents = re.findall(r'temporal<array> fridgeContents = \[(.*?)\]', self.source, re.DOTALL)
        if contents:
            entries = contents[0].split("},")
            for entry in entries:
                name_match = re.search(r'name: "(.*?)"', entry)
                added_match = re.search(r'added: "(.*?)"', entry)
                expires_match = re.search(r'expires: "(.*?)"', entry)
                if name_match and added_match and expires_match:
                    self.fridge.append({
                        "name": name_match.group(1),
                        "added": datetime.strptime(added_match.group(1), "%Y-%m-%d"),
                        "expires": datetime.strptime(expires_match.group(1), "%Y-%m-%d")
                    })

    def run_architect(self):
        print("Running architect block...")
        today = datetime.today()
        expiring = [item for item in self.fridge if (item['expires'] - today).days <= 1]
        if self.reminders_enabled and expiring:
            print("Reminder: The following leftovers are expiring soon:")
            for item in expiring:
                days_left = (item['expires'] - today).days
                print(f" - {item['name']} (expires in {days_left} day{'s' if days_left != 1 else ''})")

    def run_say_commands(self):
        say_lines = re.findall(r'say\s+\"(.*?)\"', self.source)
        for line in say_lines:
            print(f"(Slang) {line}")

    def run(self):
        print("Starting Slang prototype interpreter...")
        self.parse_temporal_contents()
        self.run_say_commands()
        self.run_architect()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Execute .slang files with CI awareness')
    parser.add_argument('file', help='.slang file to execute')
    parser.add_argument('--ci', type=float, default=0.5, help='CI level (0.0 to 1.0)')
    parser.add_argument('--function', help='Function to execute')
    parser.add_argument('--input', help='Input for the function')
    args = parser.parse_args()
    
    interpreter = SlangInterpreter(ci_level=args.ci)
    
    print(f"\nLoading {args.file} (CI Level: {args.ci})...")
    if interpreter.load_file(args.file):
        print("✓ File loaded successfully")
        
        if args.function:
            print(f"\nExecuting function: {args.function}")
            result = interpreter.execute_function(args.function, args.input)
            print(f"Result: {result}")
            
        print("\nSignals:")
        for signal in interpreter.get_signals():
            print(f"  > {signal}")
    else:
        print("✗ Failed to load file")

if __name__ == "__main__":
    main()