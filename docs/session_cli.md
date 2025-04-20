# Session CLI Usage

The `slang_session_cli.py` tool provides subcommands to manage handshake sessions.

Commands:

- `hang`
  Initiate a handshake (hang) by creating a `.slang` invitation.
```bash
python3 slang_session_cli.py hang \
    --source <YourAI> \
    --target <ServiceAI> \
    --payload payload.json \
    --output hang.slang \
    [--config profiles.json]
```

- `catch`
  Respond to a handshake by creating a `.slang` acknowledgment.
```bash
python3 slang_session_cli.py catch \
    --handshake hang.slang \
    --profile ServiceAI_profile.json \
    --output catch.slang
```

- `status`
  Query the metadata of an existing session.
```bash
python3 slang_session_cli.py status --session <session_id>
```

- `complete`
  Mark a session as completed.
```bash
python3 slang_session_cli.py complete --session <session_id>
```

- `expire`
  Mark a session as expired.
```bash
python3 slang_session_cli.py expire --session <session_id>
```

Session metadata is stored in `sessions.json` in the current working directory.