import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import re
import random
from dotenv import load_dotenv
from openai_interface import OpenAIInterface

class SlangAssistant:
    def __init__(self, user_ci_level: float = 0.5):
        # Load environment variables
        load_dotenv()
        
        self.user_ci_level = user_ci_level
        self.current_draft = {
            "system": "",
            "version": "1.0",
            "description": "",
            "context": {
                "user_ci_score": user_ci_level,
                "capabilities": [],
                "preferences": {}
            },
            "functions": []
        }
        self.conversation_history = []
        
        # Initialize OpenAI interface if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.ai_interface = OpenAIInterface(api_key=api_key)
        else:
            self.ai_interface = None
            print("(W)arning: OPENAI_API_KEY not found in .env file 😅")
        
        # EIRS-style response templates
        self._greetings = [
            "(H)ey! Let's create something epic! 🚀",
            "(W)hat's up! Ready to build? 🛠️",
            "(Y)o! Time to make magic! ✨"
        ]
        
        self._function_prompts = {
            "low": [
                "(S)imple function - tell me what it should do",
                "(B)asic task - describe it in your words",
                "(E)asy feature - what's the main idea?"
            ],
            "medium": [
                "(C)reate a system - what's the big picture?",
                "(A)dd a function - name and purpose?",
                "(D)esign feature - what should it handle?"
            ],
            "high": [
                "(A)rchitect system - define the structure",
                "(B)uild complex function - specify details",
                "(O)ptimize feature - what's the goal?"
            ]
        }
        
        self._encouragements = [
            "(N)ice thinking!",
            "(C)ool idea!",
            "(A)wesome direction!",
            "(G)reat start!"
        ]
        
    def process_user_input(self, user_input: str) -> str:
        """Process user input using EIRS principles and OpenAI interface."""
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # If we have OpenAI interface and loaded .slang file, use it
        if self.ai_interface and self.ai_interface.current_slang:
            return self.ai_interface.process_input(user_input)
            
        # Otherwise, handle draft creation
        first_letter = user_input[0].upper() if user_input else ""
        
        # Handle based on CI level
        if self.user_ci_level < 0.3:
            return self._handle_low_ci_input(user_input, first_letter)
        elif self.user_ci_level < 0.6:
            return self._handle_medium_ci_input(user_input, first_letter)
        else:
            return self._handle_high_ci_input(user_input, first_letter)
            
    def _handle_low_ci_input(self, user_input: str, first_letter: str) -> str:
        """Handle low CI input with simple EIRS options."""
        if not self.conversation_history or len(self.conversation_history) == 1:
            return random.choice(self._greetings) + "\n" + \
                   "\n".join(self._function_prompts["low"])
                   
        if first_letter in ['S', 'B', 'E']:
            return self._create_simple_function(user_input)
            
        return f"{random.choice(self._encouragements)}\n" + \
               "\n".join(self._function_prompts["low"])
               
    def _handle_medium_ci_input(self, user_input: str, first_letter: str) -> str:
        """Handle medium CI input with structured EIRS options."""
        if not self.current_draft["system"]:
            if first_letter == 'C':
                system_match = re.search(r"system\s+called\s+(\w+)", user_input.lower())
                if system_match:
                    self.current_draft["system"] = system_match.group(1)
                    return f"(R)ad! 🎸 System {system_match.group(1)} created!\n" + \
                           "\n".join(self._function_prompts["medium"])
            return "\n".join(self._function_prompts["medium"])
            
        if first_letter in ['A', 'D']:
            return self._create_medium_function(user_input)
            
        return f"{random.choice(self._encouragements)}\n" + \
               "\n".join(self._function_prompts["medium"])
               
    def _handle_high_ci_input(self, user_input: str, first_letter: str) -> str:
        """Handle high CI input with advanced EIRS options."""
        if not self.current_draft["system"]:
            if first_letter == 'A':
                system_match = re.search(r"system\s+called\s+(\w+)", user_input.lower())
                if system_match:
                    self.current_draft["system"] = system_match.group(1)
                    return f"(E)pic! 🚀 {system_match.group(1)} system initialized!\n" + \
                           "\n".join(self._function_prompts["high"])
            return "\n".join(self._function_prompts["high"])
            
        if first_letter in ['B', 'O']:
            return self._create_advanced_function(user_input)
            
        return f"{random.choice(self._encouragements)}\n" + \
               "\n".join(self._function_prompts["high"])
               
    def _create_simple_function(self, description: str) -> str:
        """Create a simple function with EIRS feedback."""
        words = description.split()
        function_name = "_".join(words[:2]).lower()
        
        function = {
            "name": function_name,
            "agent": "BasicProcessor",
            "intent": description,
            "context": {"complexity": "low"},
            "input": "text",
            "output": "processed_text"
        }
        
        self.current_draft["functions"].append(function)
        return f"(N)ice! 🎉 Created {function_name}\n" + \
               "(A)dd another function\n" + \
               "(S)ave system\n" + \
               "(Q)uit"
               
    def _create_medium_function(self, description: str) -> str:
        """Create a medium complexity function with EIRS feedback."""
        name_match = re.search(r"called\s+(\w+)", description.lower())
        if name_match:
            name = name_match.group(1)
            function = {
                "name": name,
                "agent": "MediumProcessor",
                "intent": description,
                "context": {"complexity": "medium"},
                "input": "structured_text",
                "output": "analyzed_result"
            }
            self.current_draft["functions"].append(function)
            return f"(C)ool! 🎯 Added {name}\n" + \
                   "(A)dd another function\n" + \
                   "(S)ave system\n" + \
                   "(Q)uit"
        return "(T)ry again with a function name"
        
    def _create_advanced_function(self, description: str) -> str:
        """Create an advanced function with EIRS feedback."""
        name_match = re.search(r"called\s+(\w+)", description.lower())
        if name_match:
            name = name_match.group(1)
            function = {
                "name": name,
                "agent": "AdvancedProcessor",
                "intent": description,
                "context": {"complexity": "high"},
                "input": "complex_text",
                "output": "analyzed_result"
            }
            self.current_draft["functions"].append(function)
            return f"(E)pic! 💫 Added {name}\n" + \
                   "(A)dd another function\n" + \
                   "(S)ave system\n" + \
                   "(Q)uit"
        return "(T)ry again with a function name"
        
    def save_draft(self, filename: str) -> str:
        """Save draft and load it into OpenAI interface."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.current_draft, f, indent=2)
            
            # Load the saved file into OpenAI interface if available
            if self.ai_interface and self.ai_interface.load_slang(filename):
                return f"(S)aved! 🎯 File: {filename}\n" + \
                       "(O)penAI interface loaded and ready! 🤖"
            else:
                return f"(S)aved! 🎯 File: {filename}\n" + \
                       "(N)ote: OpenAI interface not configured"
                
        except Exception as e:
            return f"(E)rror saving: {str(e)} 😅"
            
    def get_current_draft(self) -> Dict:
        """Get the current draft of the .slang file."""
        return self.current_draft
        
    def reset_draft(self) -> None:
        """Reset the current draft and OpenAI interface."""
        self.current_draft = {
            "system": "",
            "version": "1.0",
            "description": "",
            "context": {
                "user_ci_score": self.user_ci_level,
                "capabilities": [],
                "preferences": {}
            },
            "functions": []
        }
        self.conversation_history = []
        if self.ai_interface:
            self.ai_interface.reset()
            
    def set_openai_api_key(self, api_key: str = None) -> str:
        """Set OpenAI API key from environment or provided value."""
        try:
            # Use provided key or get from environment
            key = api_key or os.getenv("OPENAI_API_KEY")
            if not key:
                return "(E)rror: No API key provided! 😅"
                
            self.ai_interface = OpenAIInterface(api_key=key)
            return "(A)PI key set! OpenAI interface ready! 🚀"
        except Exception as e:
            return f"(E)rror setting API key: {str(e)} 😅" 