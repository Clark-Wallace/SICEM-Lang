"""
download_tool.py:
High-level wrapper functions for receiving and handshake response (.catch) operations using SlangReceiver.
"""
import json
from pathlib import Path

from slang_receiver import SlangReceiver
from slang_uploader import IntelligenceProfile

def receive_slang_file(transmission_file: str, profile_file: str, output_log: str = None):
    """
    Receive and process a .slang transmission file.

    :param transmission_file: Path to the transmission JSON file.
    :param profile_file: Path to the intelligence profile JSON file.
    :param output_log: Optional path to save the reception log.
    :returns: Tuple(success: bool, details: dict, log_path or None)
    """
    profile = IntelligenceProfile(**json.load(open(profile_file)))
    receiver = SlangReceiver(profile)
    status = receiver.receive_transmission(transmission_file)
    log_path = None
    if status.success and output_log:
        receiver.save_reception_log(output_log)
        log_path = output_log
    return status.success, status.details, log_path

def catch_hang_response(handshake_file: str, profile_file: str, output: str) -> str:
    """
    Respond to a 'hang' .slang handshake by generating a 'catch' .slang file.

    :param handshake_file: Path to the hang .slang file.
    :param profile_file: Path to the intelligence profile JSON file.
    :param output: Path to write the catch .slang file.
    :returns: session_id from the handshake.
    """
    profile = IntelligenceProfile(**json.load(open(profile_file)))
    receiver = SlangReceiver(profile)
    session_id = receiver.catch_hang(handshake_file, output)
    return session_id