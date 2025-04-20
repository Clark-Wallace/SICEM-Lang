# Toolbox: Reusable AI Tools for Slang

This package provides a set of Python modules for working with Slang sessions, including uploading, downloading, and session lifecycle management.

Modules:
  * upload_tool.py
    - upload_slang_file(file_path, source, target, output, config=None)
    - send_hang_request(source, target, payload, output, config=None)

  * download_tool.py
    - receive_slang_file(transmission_file, profile_file, output_log=None)
    - catch_hang_response(handshake_file, profile_file, output)

  * session_tool.py
    - new_session(participants, payload)
    - confirm_existing_session(session_id)
    - lookup_session(session_id)

Usage Examples:
```python
# Upload and adapt a .slang file
from Toolbox.upload_tool import upload_slang_file
adapted_path, log_path = upload_slang_file(
    file_path="order_flow.slang",
    source="UserAI",
    target="ServiceAI",
    output="order_flow_adapted.slang",
    config="profiles.json"
)

# Send a handshake invite
from Toolbox.upload_tool import send_hang_request
session_id = send_hang_request(
    source="UserAI",
    target="ServiceAI",
    payload={"task":"book_room","budget":100},
    output="hang.slang",
    config="profiles.json"
)

# Respond to a handshake invite
from Toolbox.download_tool import catch_hang_response
session_id = catch_hang_response(
    handshake_file="hang.slang",
    profile_file="service_profile.json",
    output="catch.slang"
)

# Inspect session metadata
from Toolbox.session_tool import lookup_session
metadata = lookup_session(session_id)
print(metadata)
``` 

Ensure that the `Toolbox` directory is on your Python path (e.g., via `PYTHONPATH=.`).