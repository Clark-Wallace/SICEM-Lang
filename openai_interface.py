from typing import Dict, Any, Optional, List
from openai import OpenAI
import json
from ai_interface import AIInterface

class OpenAIInterface(AIInterface):
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        super().__init__(model_name)
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        
    def load_slang(self, slang_file: str) -> bool:
        """Load a .slang file and validate its structure."""
        try:
            with open(slang_file, 'r') as f:
                self.current_slang = json.load(f)
            return self._validate_slang()
        except Exception as e:
            print(f"(E)rror loading .slang file: {str(e)} 😅")
            return False
            
    def _validate_slang(self) -> bool:
        """Validate the loaded .slang file structure."""
        required_fields = ["system", "version", "description", "context", "functions"]
        if not all(field in self.current_slang for field in required_fields):
            return False
        return True
        
    def process_input(self, user_input: str) -> str:
        """Process user input using OpenAI's API."""
        if not self.current_slang:
            return "(E)rror: No .slang file loaded! 😅"
            
        # Prepare the system message from .slang file
        system_message = self._create_system_message()
        
        # Prepare conversation history
        messages = [
            {"role": "system", "content": system_message}
        ] + self.conversation_history[-5:]  # Keep last 5 messages for context
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Get the response
            ai_response = response.choices[0].message.content
            
            # Add to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"(E)rror with OpenAI API: {str(e)} 😅"
            
    def _create_system_message(self) -> str:
        """Create a system message from the .slang file."""
        if not self.current_slang:
            return ""
            
        # Build system message
        system_parts = [
            f"You are {self.current_slang['system']}.",
            f"Version: {self.current_slang['version']}",
            f"Description: {self.current_slang['description']}",
            "\nCapabilities:",
            *[f"- {cap}" for cap in self.current_slang['context']['capabilities']],
            "\nFunctions:",
            *[f"- {func['name']}: {func['intent']}" for func in self.current_slang['functions']],
            "\nPreferences:",
            *[f"- {k}: {v}" for k, v in self.current_slang['context']['preferences'].items()],
            "\nRespond in EIRS style with (L)etter format for quick actions."
        ]
        
        return "\n".join(system_parts)
        
    def _process_low_ci(self, user_input: str) -> str:
        """Process input for low CI level using OpenAI."""
        return self.process_input(
            f"Keep it simple and friendly. User input: {user_input}"
        )
        
    def _process_medium_ci(self, user_input: str) -> str:
        """Process input for medium CI level using OpenAI."""
        return self.process_input(
            f"Provide detailed but clear explanation. User input: {user_input}"
        )
        
    def _process_high_ci(self, user_input: str) -> str:
        """Process input for high CI level using OpenAI."""
        return self.process_input(
            f"Provide in-depth technical analysis. User input: {user_input}"
        ) 