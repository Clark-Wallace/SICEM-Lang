import re
import yaml
from typing import Dict, List, Any, Optional
from signal_transmitter import SignalTransmitter, Signal, SignalType

class SlangParser:
    def __init__(self):
        self.system: Dict[str, Any] = {}
        self.functions: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        
    def parse_system(self, content: str) -> Dict[str, Any]:
        """Parse the system name from .slang content"""
        # Extract the system name (first token after 'system:'), allowing leading whitespace
        match = re.search(r'^\s*system:\s*(\S+)', content, re.MULTILINE)
        name = match.group(1).strip() if match else ''
        # We only need the system name for downstream generation
        self.system = {'name': name}
        return self.system
    
    def parse_functions(self, content: str) -> List[Dict[str, Any]]:
        """Parse function blocks from .slang content"""
        # Regex to capture function blocks with optional indented context
        pattern = re.compile(
            r'function:\s*(?P<name>\w+)\s*'
            r'agent:\s*(?P<agent>\w+)\s*'
            r'intent:\s*(?P<intent>[^\n]+)'  # up to end of line
            r'(?:\s*context:\s*(?P<context>(?:[ \t]+.*\n)*))?'  # optional indented context lines
            r'\s*input:\s*(?P<input>[^\n]+)\s*'  # single-line input
            r'output:\s*(?P<output>[^\n]+)',
            re.MULTILINE
        )
        # Clear previous functions
        self.functions = []
        for match in pattern.finditer(content):
            # Parse context block if present
            ctx_text = match.group('context') or ''
            # Remove leading indentation for YAML parsing
            ctx_clean = '\n'.join(line.lstrip() for line in ctx_text.splitlines())
            context = yaml.safe_load(ctx_clean) if ctx_clean else {}
            # Output is a simple token, keep as string
            output_val = match.group('output').strip()
            function = {
                'name': match.group('name').strip(),
                'agent': match.group('agent').strip(),
                'intent': match.group('intent').strip(),
                'context': context,
                'input': match.group('input').strip(),
                'output': output_val
            }
            self.functions.append(function)
        return self.functions
    
    def parse(self, content: str) -> Dict[str, Any]:
        """Parse entire .slang content"""
        self.parse_system(content)
        self.parse_functions(content)
        
        return {
            'system': self.system,
            'functions': self.functions
        }

class SlangInterpreter:
    def __init__(self, parser: SlangParser):
        self.parser = parser
        self.ci_level: float = 0.5  # Default CI level
        self.context: Dict[str, Any] = {}
        self.transmitter = SignalTransmitter()
        
    def set_ci_level(self, level: float):
        """Set the Contextual Intelligence level"""
        self.ci_level = max(0.1, min(1.0, level))
        
    def interpret_function(self, function: Dict[str, Any]) -> str:
        """Interpret a function based on CI level"""
        # Create a signal for the function
        signal = Signal(
            type=SignalType.EXPLANATION,
            content=f"{function['name']} {function['intent']}",
            source_ci=1.0,  # Assume source is at maximum CI
            target_ci=self.ci_level,
            metadata={
                "agent": function['agent'],
                "input": function['input'],
                "output": function['output']
            }
        )
        
        # Transmit and adapt the signal
        return self.transmitter.transmit(signal)
    
    def run(self, content: str) -> Dict[str, Any]:
        """Run the interpreter on .slang content"""
        parsed = self.parser.parse(content)
        results = []
        
        for function in parsed['functions']:
            explanation = self.interpret_function(function)
            results.append({
                'function': function['name'],
                'explanation': explanation
            })
        
        return {
            'system': parsed['system'],
            'results': results,
            'signal_history': self.transmitter.get_signal_history()
        } 