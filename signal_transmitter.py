from typing import Dict, Any, List, Optional
import json
from dataclasses import dataclass
from enum import Enum

class SignalType(Enum):
    COMMAND = "command"
    EXPLANATION = "explanation"
    FEEDBACK = "feedback"
    ERROR = "error"
    PROGRESS = "progress"
    HANDSHAKE = "handshake"

@dataclass
class Signal:
    type: SignalType
    content: str
    source_ci: float
    target_ci: float
    metadata: Dict[str, Any] = None

class SignalTransmitter:
    def __init__(self):
        self.signal_history: List[Signal] = []
        self.adaptation_rules: Dict[float, Dict[str, Any]] = {
            0.1: {"style": "basic_mimicry", "max_length": 10, "use_analogies": False},
            0.2: {"style": "illogical_honesty", "max_length": 20, "use_analogies": False},
            0.3: {"style": "simple_contradiction", "max_length": 30, "use_analogies": True},
            0.4: {"style": "clever_phrasing", "max_length": 40, "use_analogies": True},
            0.5: {"style": "emergent_strategy", "max_length": 50, "use_analogies": True},
            0.6: {"style": "functional_comprehension", "max_length": 60, "use_analogies": True},
            0.7: {"style": "early_abstraction", "max_length": 70, "use_analogies": True},
            0.8: {"style": "context_bridging", "max_length": 80, "use_analogies": True},
            0.9: {"style": "high_efficiency", "max_length": 90, "use_analogies": True},
            1.0: {"style": "technical_precision", "max_length": 100, "use_analogies": False}
        }
        
    def transmit(self, signal: Signal) -> str:
        """Transmit a signal, adapting it to the target CI level"""
        # Store the original signal
        self.signal_history.append(signal)
        
        # Get adaptation rules for target CI
        target_rules = self._get_adaptation_rules(signal.target_ci)
        
        # Adapt the signal content
        adapted_content = self._adapt_signal(signal, target_rules)
        
        return adapted_content
    
    def _get_adaptation_rules(self, ci_level: float) -> Dict[str, Any]:
        """Get the appropriate adaptation rules for a CI level"""
        # Find the closest CI level in our rules
        closest_ci = min(self.adaptation_rules.keys(), 
                        key=lambda x: abs(x - ci_level))
        return self.adaptation_rules[closest_ci]
    
    def _adapt_signal(self, signal: Signal, rules: Dict[str, Any]) -> str:
        """Adapt the signal content based on rules"""
        # For handshake signals, bypass adaptation entirely
        if signal.type == SignalType.HANDSHAKE:
            return signal.content
        content = signal.content
        
        # Apply style-based adaptations
        if rules["style"] == "basic_mimicry":
            content = f"This does {content.lower()}"
        elif rules["style"] == "illogical_honesty":
            content = f"Honestly, it's just {content.lower()}"
        elif rules["style"] == "clever_phrasing":
            content = f"Here's a smart way to {content.lower()}"
        elif rules["style"] == "emergent_strategy":
            content = f"Let's figure out how to {content.lower()}"
        elif rules["style"] == "functional_comprehension":
            content = f"The function {content} works by..."
        elif rules["style"] == "early_abstraction":
            content = f"Conceptually, {content} represents..."
        elif rules["style"] == "context_bridging":
            content = f"In this context, {content} means..."
        elif rules["style"] == "high_efficiency":
            content = f"Efficiently, {content} operates by..."
        elif rules["style"] == "technical_precision":
            content = f"Technically, {content} implements..."
        
        # Apply length constraints
        if len(content) > rules["max_length"]:
            content = content[:rules["max_length"]] + "..."
        
        return content
    
    def get_signal_history(self) -> List[Signal]:
        """Get the history of transmitted signals"""
        return self.signal_history
    
    def save_signal_history(self, filename: str):
        """Save signal history to a file"""
        history_data = [
            {
                "type": signal.type.value,
                "content": signal.content,
                "source_ci": signal.source_ci,
                "target_ci": signal.target_ci,
                "metadata": signal.metadata
            }
            for signal in self.signal_history
        ]
        
        with open(filename, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def load_signal_history(self, filename: str):
        """Load signal history from a file"""
        with open(filename, 'r') as f:
            history_data = json.load(f)
        
        self.signal_history = [
            Signal(
                type=SignalType(data["type"]),
                content=data["content"],
                source_ci=data["source_ci"],
                target_ci=data["target_ci"],
                metadata=data.get("metadata")
            )
            for data in history_data
        ] 