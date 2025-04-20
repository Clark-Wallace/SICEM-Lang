from typing import Dict, Any, List, Optional
import json
from pathlib import Path
from dataclasses import dataclass
from signal_transmitter import SignalTransmitter, Signal, SignalType
from slang_parser import SlangParser, SlangInterpreter

@dataclass
class ReceptionStatus:
    success: bool
    message: str
    details: Dict[str, Any] = None

class SlangReceiver:
    def __init__(self, intelligence_profile):
        self.profile = intelligence_profile
        self.transmitter = SignalTransmitter()
        self.parser = SlangParser()
        self.interpreter = SlangInterpreter(self.parser)
        self.received_files: List[Dict[str, Any]] = []
        
    def receive_transmission(self, transmission_file: str) -> ReceptionStatus:
        """Receive and process a transmission file"""
        try:
            # Load the transmission
            with open(transmission_file, 'r') as f:
                transmission = json.load(f)
                
            # Validate the transmission is for this intelligence
            if transmission['target'] != self.profile.name:
                return ReceptionStatus(
                    success=False,
                    message=f"Transmission intended for {transmission['target']}, but received by {self.profile.name}",
                    details={"expected": transmission['target'], "actual": self.profile.name}
                )
                
            # Process the adapted content
            processed_content = self._process_adaptations(transmission['adaptations'])
            
            # Store the received file
            self.received_files.append({
                'transmission': transmission,
                'processed_content': processed_content,
                'timestamp': json.loads(transmission['metadata'])['timestamp'] if 'metadata' in transmission else None
            })
            
            return ReceptionStatus(
                success=True,
                message="Transmission successfully received and processed",
                details={
                    'source': transmission['source'],
                    'functions_processed': len(processed_content),
                    'ci_level': transmission['target_ci']
                }
            )
            
        except Exception as e:
            return ReceptionStatus(
                success=False,
                message=f"Error processing transmission: {str(e)}",
                details={'error': str(e)}
            )
    
    def _process_adaptations(self, adaptations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process the adapted content for this intelligence"""
        processed = []
        
        for adaptation in adaptations:
            # Create a signal to verify the adaptation
            signal = Signal(
                type=SignalType.EXPLANATION,
                content=adaptation['adapted'],
                source_ci=self.profile.ci_level,
                target_ci=self.profile.ci_level,
                metadata={
                    'original': adaptation['original'],
                    'capabilities': self.profile.capabilities
                }
            )
            
            # Verify the adaptation is appropriate
            verified_content = self.transmitter.transmit(signal)
            
            processed.append({
                'original': adaptation['original'],
                'received': adaptation['adapted'],
                'verified': verified_content,
                'capability_check': self._check_capabilities(adaptation['original'])
            })
            
        return processed
    
    def _check_capabilities(self, function: Dict[str, Any]) -> Dict[str, bool]:
        """Check if this intelligence has the required capabilities"""
        required_capabilities = {
            'natural_language': ['interpret_user_intent', 'explain_task_blocks'],
            'code_generation': ['translate_to_task_blocks', 'implement_functions'],
            'context_understanding': ['monitor_context_curiosity', 'adapt_to_context']
        }
        
        checks = {}
        for capability, functions in required_capabilities.items():
            if capability in self.profile.capabilities:
                checks[capability] = any(func in function['name'] for func in functions)
            else:
                checks[capability] = False
                
        return checks
    
    def get_received_files(self) -> List[Dict[str, Any]]:
        """Get all received and processed files"""
        return self.received_files
    
    def save_reception_log(self, output_path: str):
        """Save a log of all received files"""
        log_data = {
            'receiver_profile': {
                'name': self.profile.name,
                'ci_level': self.profile.ci_level,
                'capabilities': self.profile.capabilities
            },
            'received_files': self.received_files
        }
        
        with open(output_path, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def catch_hang(self, handshake_file: str, output_path: str) -> str:
        """
        Process an incoming 'hang' handshake .slang file and generate a 'catch' response.
        Returns the session_id.
        """
        from pathlib import Path
        import re
        from session_manager import confirm_session

        # Read hang content
        content = Path(handshake_file).read_text()
        # Verify HMAC signature
        import os, hmac, hashlib
        secret = os.getenv("SLANG_HMAC_SECRET")
        if not secret:
            raise RuntimeError("Environment variable SLANG_HMAC_SECRET is not set")
        sig_match = re.search(r'signature:\s*"([^"]+)"', content)
        if not sig_match:
            raise ValueError(f"Missing signature in {handshake_file}")
        signature = sig_match.group(1)
        # Compute expected signature over the content before the signature line
        body = content[:sig_match.start()]
        expected = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("Signature verification failed for handshake file")
        # Content is verified; proceed

        # Extract session_id
        # Extract session_id from hang file (e.g., session_id: "...")
        match = re.search(r'session_id:\s*"([^\"]+)"', content)
        if not match:
            raise ValueError(f"Could not find session_id in {handshake_file}")
        session_id = match.group(1)

        # Confirm the session
        confirm_session(session_id)

        # Build catch .slang content
        slang = []
        slang.append("system: Handshake")
        slang.append("function: catch")
        slang.append(f"agent: {self.profile.name}")
        slang.append("intent: accept_session")
        slang.append("context:")
        slang.append(f"  session_id: \"{session_id}\"")
        slang.append("output: status:confirmed")
        content_out = "\n".join(slang) + "\n"

        # Write to file
        Path(output_path).write_text(content_out)
        return session_id
    
    def load_reception_log(self, file_path: str):
        """Load a previously saved reception log"""
        with open(file_path, 'r') as f:
            log_data = json.load(f)
            
        self.received_files = log_data['received_files'] 