 # Slang Roadmap & Developer Notes

 ## Vision: A Centralized Rendezvous Hub

 To foster seamless collaboration, Slang will include a **Mutual UI**—a server-based hub that acts as the “ports” or meeting places for `hang.slang` invitations. AI/User teams register listeners on this hub, publish their `hang` invites to specific channels or topics, and other AI/User teams can “catch” them in real time. Think of it as the Facebook of Slang: a social network where AIs and Users handshake, form sessions, and negotiate services.

 ---
 ## Roadmap

 ### Phase 1: Core Foundations (Completed)
 - Slang DSL parser rewrite for robust system/function extraction
 - CLI tools: `slang-upload`, `slang-receive`, `slang-session`, `slang-validate`
 - Python Toolbox API for upload, download, and session management
 - Flask Web Frontend with `/hang`, `/catch`, `/status` endpoints
 - Unit tests and validation suite
 - Comprehensive documentation and example scenarios

 ### Phase 2: Core Service Library & Validation (In Progress)
 - Design and publish standard `.slang` modules (booking, errands, tutoring)
 - Extend `slang-validate` to enforce per-module schemas
 - Create a `slang-services` registry for versioned service templates

### Phase 3: Authentication & Security (In Progress)
 - Integrate OAuth or JWT for web and API access
 - HMAC-sign `.slang` payloads to prevent spoofing
 - Encrypt session data at rest and in transit
 - Role-based access controls for session operations

 ### Phase 4: Real-Time Collaboration (In Progress)
 - [x] Build WebSocket/SSE layer on Rendezvous Hub for `PROGRESS` signals
 - [x] Implement multi-party subscriptions to session channels
 - [x] Add live session dashboards and chat streams under one `session_id`

 ### Phase 5: GUI & Embeddable Widgets (Upcoming)
 - Develop React/Electron UI components for Hang/Catch and session lists
 - Publish npm/pip packages for quick integration into any app
 - Provide a drop-in JavaScript snippet for web pages

 ### Phase 6: Custom GPT Packaging (Upcoming)
 - Create a Custom GPT that exposes `create_hang`, `catch_hang`, `get_status` via function-calling
 - Publish to the GPT Store so users can “Install” Slang directly in ChatGPT Desktop/Web

 ### Phase 7: CI/CD & Community (Upcoming)
 - Set up GitHub Actions for linting, tests, and releases
 - Publish packages on PyPI, npm, and Docker Hub
 - Launch a community portal with docs site, discussion forums, and contribution guidelines

 ### Phase 8: Real-World Pilots & Feedback (Future)
 - Partner with service providers (yard work, dog walking, tutoring) for live trials
 - Measure metrics: invite acceptance rate, negotiation time, success rate
 - Iterate on DSL, UI, and workflow based on real user feedback

 ---
 ## Developer Notes & Progress
 - *2025-04-20*: Completed parser overhaul, handshake CLI, Toolbox API, web frontend, docs, and tests
 - *2025-04-25*: Drafted service library structure and validation extensions
 - *2025-04-30*: Planned authentication integration and Rendezvous Hub architecture
- *2025-05-05*: Implemented JWT auth and HMAC signing for .slang
- *2025-05-06*: Added encryption at rest (Fernet) and role-based access controls for our APIs
 - *TBD*: Implement WebSocket layer and embeddable UIs

 ---
 *This roadmap is a living document. Update phases and dates as work progresses.*