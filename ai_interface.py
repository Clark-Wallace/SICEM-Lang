from typing import Dict, Any, Optional, List

class AIInterface:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.current_slang: Optional[Dict[str, Any]] = None
        self.conversation_history: List[Dict[str, str]] = []
        
    def load_slang(self, slang_file: str) -> bool:
        """Load a .slang file and validate its structure."""
        raise NotImplementedError("Subclass must implement abstract method")
        
    def process_input(self, user_input: str) -> str:
        """Process user input based on the loaded .slang file."""
        raise NotImplementedError("Subclass must implement abstract method")
        
    def _create_system_message(self) -> str:
        """Create a system message from the .slang file."""
        raise NotImplementedError("Subclass must implement abstract method")
        
    def _process_low_ci(self, user_input: str) -> str:
        """Process input for low CI level."""
        raise NotImplementedError("Subclass must implement abstract method")
        
    def _process_medium_ci(self, user_input: str) -> str:
        """Process input for medium CI level."""
        raise NotImplementedError("Subclass must implement abstract method")
        
    def _process_high_ci(self, user_input: str) -> str:
        """Process input for high CI level."""
        raise NotImplementedError("Subclass must implement abstract method")
        
    def reset(self) -> None:
        """Reset the interface state."""
        self.current_slang = None
        self.conversation_history = [] 