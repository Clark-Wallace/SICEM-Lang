# SICEM-Lang "Slang"

A Context Intelligence (CI) aware toolkit and CLI for exchanging `.slang` files between AIs, with support for session-based handshakes (`hang`/`catch`), content adaptation, and versatile signal communications.

## Features
- Parse and generate `.slang` files
- Adaptive signal transmission based on CI levels
- Handshake sessions (`hang`/`catch`) for collaborative workflows
- CLI tools: upload, receive, session, validate
- Toolbox Python API for embedding in AI agents
- Real-world examples and unit tests

## Installation
```bash
git clone <repository-url>
cd <repo-directory>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
```

## CLI Tools
- `slang-upload`: Upload and adapt a `.slang` file
- `slang-receive`: Receive and process a `.slang` transmission
- `slang-session`: Manage handshake sessions (`hang`, `catch`, `status`, `complete`, `expire`)
- `slang-validate`: Validate the structure of a `.slang` file

Refer to the `docs/` folder for detailed usage examples.

## Development
```bash
# Run unit tests
pytest
```

## Examples
See `session_examples/` for illustrative handshake scenarios.