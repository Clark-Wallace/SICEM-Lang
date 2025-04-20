"""
upload_tool.py:
High-level wrapper functions for uploading and handshake (.hang) operations using SlangUploader.
"""
import json
from pathlib import Path

from slang_uploader import SlangUploader, IntelligenceProfile

def upload_slang_file(file_path: str, source: str, target: str, output: str, config: str = None):
    """
    Upload and adapt a .slang file from source to target.

    :param file_path: Path to the original .slang file.
    :param source: Source intelligence name.
    :param target: Target intelligence name.
    :param output: Path to save the adapted .slang file.
    :param config: Optional path to intelligence configuration JSON.
    :returns: Tuple(adapted_file_path, transmission_log_path)
    """
    uploader = SlangUploader()
    # Register intelligences from config if provided
    if config:
        cfg = json.load(open(config))
        for p in cfg.get("intelligences", []):
            uploader.register_intelligence(IntelligenceProfile(**p))
    else:
        raise ValueError("Intelligence config file is required to upload a .slang file.")

    # Perform upload and adaptation
    transmission = uploader.upload_slang(file_path, source, target)
    adapted = uploader.generate_target_slang(transmission)
    # Write adapted .slang
    Path(output).write_text(adapted)
    # Save transmission log
    log_path = str(Path(file_path).with_suffix('.transmission.json'))
    uploader.save_transmission(transmission, log_path)
    return output, log_path

def send_hang_request(source: str, target: str, payload: dict, output: str, config: str = None) -> str:
    """
    Initiate a handshake session by sending a 'hang' .slang file.

    :param source: Source intelligence name.
    :param target: Target intelligence name.
    :param payload: Dictionary of invite metadata.
    :param output: Path to write the hang .slang file.
    :param config: Optional path to intelligence configuration JSON.
    :returns: Generated session_id.
    """
    uploader = SlangUploader()
    # Register intelligences
    if config:
        cfg = json.load(open(config))
        for p in cfg.get("intelligences", []):
            uploader.register_intelligence(IntelligenceProfile(**p))
    else:
        # Default minimal profiles if no config
        uploader.register_intelligence(IntelligenceProfile(source, 0.7, [], {}))
        uploader.register_intelligence(IntelligenceProfile(target, 0.7, [], {}))

    session_id = uploader.send_hang(source, target, payload, output)
    return session_id