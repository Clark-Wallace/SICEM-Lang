import argparse
import json
from pathlib import Path

from slang_uploader import SlangUploader, IntelligenceProfile
from slang_receiver import SlangReceiver

def main():
    parser = argparse.ArgumentParser(description="Session handshake CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # Hang command
    parser_hang = sub.add_parser("hang", help="Initiate a handshake session")
    parser_hang.add_argument("--source", required=True, help="Source intelligence name")
    parser_hang.add_argument("--target", required=True, help="Target intelligence name")
    parser_hang.add_argument("--payload", required=True, help="Path to JSON payload file")
    parser_hang.add_argument("--output", required=True, help="Output .slang file path")
    parser_hang.add_argument("--config", help="Optional intelligence config JSON")

    # Catch command
    parser_catch = sub.add_parser("catch", help="Respond to a handshake session")
    parser_catch.add_argument("--handshake", required=True, help="Path to hang .slang file")
    parser_catch.add_argument("--profile", required=True, help="Path to intelligence profile JSON")
    parser_catch.add_argument("--output", required=True, help="Output .slang file path")

    # Status command
    parser_status = sub.add_parser("status", help="Show session metadata")
    parser_status.add_argument("--session", required=True, help="Session ID to query")

    # Complete command
    parser_complete = sub.add_parser("complete", help="Mark session as completed")
    parser_complete.add_argument("--session", required=True, help="Session ID to complete")

    # Expire command
    parser_expire = sub.add_parser("expire", help="Mark session as expired")
    parser_expire.add_argument("--session", required=True, help="Session ID to expire")

    args = parser.parse_args()

    if args.command == "hang":
        # Load payload
        payload = json.load(open(args.payload))
        uploader = SlangUploader()
        # Register intelligences
        if args.config:
            cfg = json.load(open(args.config))
            for p in cfg.get("intelligences", []):
                uploader.register_intelligence(IntelligenceProfile(**p))
        else:
            # Default minimal profiles
            uploader.register_intelligence(IntelligenceProfile(args.source, 0.7, [], {}))
            uploader.register_intelligence(IntelligenceProfile(args.target, 0.7, [], {}))
        session_id = uploader.send_hang(args.source, args.target, payload, args.output)
        print(f"Hang created with session_id: {session_id}")
        print(f"Hang file written to: {args.output}")

    elif args.command == "catch":
        # Load catcher profile
        pf = json.load(open(args.profile))
        profile = IntelligenceProfile(**pf)
        receiver = SlangReceiver(profile)
        session_id = receiver.catch_hang(args.handshake, args.output)
        print(f"Catch created with session_id: {session_id}")
        print(f"Catch file written to: {args.output}")

    elif args.command == "status":
        # Show session metadata
        from session_manager import get_session
        meta = get_session(args.session)
        if not meta:
            print(f"Session {args.session} not found.")
            return 1
        print(json.dumps(meta, indent=2))
    elif args.command == "complete":
        # Mark session as completed
        from session_manager import complete_session
        try:
            complete_session(args.session)
            print(f"Session {args.session} marked as completed.")
        except KeyError as e:
            print(str(e))
            return 1
    elif args.command == "expire":
        # Mark session as expired
        from session_manager import expire_session
        try:
            expire_session(args.session)
            print(f"Session {args.session} marked as expired.")
        except KeyError as e:
            print(str(e))
            return 1
    else:
        parser.print_help()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())