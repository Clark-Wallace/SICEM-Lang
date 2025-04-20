from typing import Dict, Any, List, Optional
import json
from pathlib import Path
from dataclasses import dataclass
from signal_transmitter import SignalTransmitter, Signal, SignalType
from slang_parser import SlangParser, SlangInterpreter
from cil_tracker import CILTracker, CILAssessment

@dataclass
class IntelligenceProfile:
    name: str
    ci_level: float
    capabilities: List[str]
    preferences: Dict[str, Any]
    metadata: Dict[str, Any] = None

class SlangUploader:
    def __init__(self):
        self.transmitter = SignalTransmitter()
        self.parser = SlangParser()
        self.interpreter = SlangInterpreter(self.parser)
        self.known_intelligences: Dict[str, IntelligenceProfile] = {}
        self.cil_tracker = CILTracker()
        
    def register_intelligence(self, profile: IntelligenceProfile):
        """Register a new intelligence in the system"""
        self.known_intelligences[profile.name] = profile
        
        # Initialize CIL tracking if not already present
        if not self.cil_tracker.get_current_cil(profile.name):
            self.cil_tracker.track_interaction(profile.name, {
                'initial_registration': True,
                'context_understanding': {'score': 0.5},
                'content_adaptation': {'effectiveness': 0.5},
                'learning_progress': {'improvement': 0.0},
                'communication': {'clarity': 0.5},
                'problem_solving': {'innovation': 0.5}
            })
        
    def upload_slang(self, file_path: str, source_intelligence: str, target_intelligence: str) -> Dict[str, Any]:
        """Upload and transmit a .slang file between intelligences"""
        # Validate intelligences
        if source_intelligence not in self.known_intelligences:
            raise ValueError(f"Unknown source intelligence: {source_intelligence}")
        if target_intelligence not in self.known_intelligences:
            raise ValueError(f"Unknown target intelligence: {target_intelligence}")
            
        source = self.known_intelligences[source_intelligence]
        target = self.known_intelligences[target_intelligence]
        
        # Get current CIL assessments
        source_cil = self.cil_tracker.get_current_cil(source.name)
        target_cil = self.cil_tracker.get_current_cil(target.name)
        
        # Use CIL scores if available, otherwise use profile CI levels
        source_ci = source_cil.overall_score if source_cil else source.ci_level
        target_ci = target_cil.overall_score if target_cil else target.ci_level
        
        # Read and parse the .slang file
        with open(file_path, 'r') as f:
            content = f.read()
            
        parsed = self.parser.parse(content)
        
        # Create transmission package
        transmission = {
            "source": source.name,
            "target": target.name,
            "source_ci": source_ci,
            "target_ci": target_ci,
            "original_content": content,
            "parsed_content": parsed,
            "adaptations": [],
            "cil_metadata": {
                "source_assessment": source_cil.metrics.__dict__ if source_cil else None,
                "target_assessment": target_cil.metrics.__dict__ if target_cil else None
            }
        }
        
        # Adapt each function for the target intelligence
        for function in parsed['functions']:
            # Create signal for the function
            signal = Signal(
                type=SignalType.EXPLANATION,
                content=json.dumps(function),
                source_ci=source_ci,
                target_ci=target_ci,
                metadata={
                    "source_capabilities": source.capabilities,
                    "target_capabilities": target.capabilities,
                    "source_preferences": source.preferences,
                    "target_preferences": target.preferences,
                    "cil_metrics": {
                        "source": source_cil.metrics.__dict__ if source_cil else None,
                        "target": target_cil.metrics.__dict__ if target_cil else None
                    }
                }
            )
            
            # Transmit and adapt the signal
            adapted = self.transmitter.transmit(signal)
            transmission["adaptations"].append({
                "original": function,
                "adapted": adapted
            })
            
            # Track the interaction for CIL assessment
            self._track_interaction(source.name, target.name, function, adapted)
            
        return transmission
    
    def _track_interaction(self, source: str, target: str, function: Dict[str, Any], adapted: str):
        """Track the interaction for CIL assessment"""
        # Track source intelligence interaction
        self.cil_tracker.track_interaction(source, {
            'context_understanding': {
                'score': 1.0 if function.get('context') else 0.5
            },
            'content_adaptation': {
                'effectiveness': 1.0 if adapted != json.dumps(function) else 0.5
            },
            'communication': {
                'clarity': 1.0 if len(adapted) > 0 else 0.0
            }
        })
        
        # Track target intelligence interaction
        self.cil_tracker.track_interaction(target, {
            'context_understanding': {
                'score': 1.0 if 'context' in adapted else 0.5
            },
            'learning_progress': {
                'improvement': 0.1  # Small improvement for receiving new information
            }
        })
    
    def save_transmission(self, transmission: Dict[str, Any], output_path: str):
        """Save a transmission to a file"""
        with open(output_path, 'w') as f:
            json.dump(transmission, f, indent=2)
            
    def send_hang(self, source: str, target: str, payload: Dict[str, Any], output_path: str) -> str:
        """
        Initiate a handshake session by sending a 'hang' .slang file.
        Returns the generated session_id.
        """
        from session_manager import create_session
        from pathlib import Path

        # Create a new session
        session_id = create_session([source, target], payload)

        # Build the hang .slang content
        slang = []
        slang.append(f"system: Handshake")
        slang.append(f"function: hang")
        slang.append(f"agent: {source}")
        slang.append(f"intent: invite_to_session")
        slang.append("context:")
        slang.append(f"  session_id: \"{session_id}\"")
        slang.append(f"  participants:")
        slang.append(f"    - \"{source}\"")
        slang.append(f"    - \"{target}\"")
        slang.append(f"  payload: {json.dumps(payload)}")
        slang.append(f"output: session:{session_id}")
        # Render initial .slang content
        content = "\n".join(slang) + "\n"
        # Sign the content with HMAC to prevent tampering
        import os, hmac, hashlib
        secret = os.getenv("SLANG_HMAC_SECRET")
        if not secret:
            raise RuntimeError("Environment variable SLANG_HMAC_SECRET is not set")
        signature = hmac.new(secret.encode(), content.encode(), hashlib.sha256).hexdigest()
        # Append signature line
        content += f"signature: \"{signature}\"\n"
        # Write to file
        Path(output_path).write_text(content)
        return session_id
    def load_transmission(self, file_path: str) -> Dict[str, Any]:
        """Load a transmission from a file"""
        with open(file_path, 'r') as f:
            return json.load(f)
            
    def generate_target_slang(self, transmission: Dict[str, Any]) -> str:
        """Generate a .slang file for the target intelligence"""
        target = self.known_intelligences[transmission["target"]]
        
        # Start with system definition
        slang_content = f"system: {transmission['parsed_content']['system']['name']}\n"
        slang_content += f"context:\n  user_ci_score: {target.ci_level}\n"
        
        # Add adapted functions
        for adaptation in transmission["adaptations"]:
            original = adaptation["original"]
            slang_content += f"\nfunction: {original['name']}\n"
            slang_content += f"agent: {original['agent']}\n"
            slang_content += f"intent: {original['intent']}\n"
            if original.get('context'):
                slang_content += f"context: {json.dumps(original['context'])}\n"
            slang_content += f"input: {original['input']}\n"
            slang_content += f"output: {original['output']}\n"
            
        return slang_content 