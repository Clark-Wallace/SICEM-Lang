class SlangInterpreter:
    def __init__(self, ci_level=0.5):
        self.ci_level = ci_level
        self.signal_transmitter = SignalTransmitter()
        
    def execute_function(self, function_def, input_text):
        """Execute a specific function with given input."""
        try:
            # Create and transmit signal for the function
            signal = Signal(
                type=SignalType.COMMAND,
                content=input_text,
                source_ci=self.ci_level,
                target_ci=self.ci_level,
                function_name=function_def['name']
            )
            
            # Transmit and adapt the signal
            adapted_signal = self.signal_transmitter.transmit(signal)
            
            # Process the function based on its type
            if function_def['name'] == 'process_text':
                return self._process_text(adapted_signal.content)
            elif function_def['name'] == 'analyze_context':
                return self._analyze_context(adapted_signal.content)
            else:
                # Simplified error message for low CI users
                if self.ci_level < 0.3:
                    return "Sorry, I don't know how to do that yet."
                else:
                    raise ValueError(f"Unknown function: {function_def['name']}")
                
        except Exception as e:
            # Simplified error handling for low CI users
            if self.ci_level < 0.3:
                return "Something went wrong. Please try again with simpler words."
            else:
                error_signal = Signal(
                    type=SignalType.ERROR,
                    content=str(e),
                    source_ci=self.ci_level,
                    target_ci=self.ci_level,
                    function_name=function_def['name']
                )
                self.signal_transmitter.transmit(error_signal)
                raise
            
    def _process_text(self, text):
        """Process text input based on CI level."""
        if self.ci_level >= 0.8:
            return f"High-level analysis: {text}"
        elif self.ci_level >= 0.6:
            return f"Detailed analysis: {text}"
        elif self.ci_level >= 0.4:
            return f"Basic analysis: {text}"
        else:
            # Simplified output for very low CI users
            return f"I understand you said: {text}"
            
    def _analyze_context(self, text):
        """Analyze context based on CI level."""
        if self.ci_level >= 0.8:
            return f"Deep context analysis: {text}"
        elif self.ci_level >= 0.6:
            return f"Contextual understanding: {text}"
        elif self.ci_level >= 0.4:
            return f"Basic context: {text}"
        else:
            # Simplified output for very low CI users
            return f"I think you're talking about: {text}"
            
    def get_help(self):
        """Get simplified help based on CI level."""
        if self.ci_level >= 0.8:
            return """
            Available functions:
            - process_text: Analyze and process text input
            - analyze_context: Understand the context of text
            """
        elif self.ci_level >= 0.6:
            return """
            You can use these functions:
            - process_text: Look at text
            - analyze_context: Understand text
            """
        elif self.ci_level >= 0.4:
            return """
            Try these:
            - process_text: Type something
            - analyze_context: Tell me about something
            """
        else:
            return """
            Type something and I'll help you.
            """ 