# KI Social Architecture

## Identity
One user identity is intended to be shared across the project family. Production authentication must issue a signed session/JWT and never trust a client-supplied user id.

## Messaging
`user` conversations connect users. `agent` conversations connect a user to one specialist agent. `assistant` is the general assistant. `bot` represents an automated topic service.

## Realtime
The API contract is REST-compatible. Production realtime delivery should use WebSocket or SSE, with authorization checked for every conversation subscription.

## Storage
Development can use SQLite. Production should use PostgreSQL. Messages should be indexed by conversation and creation time, and retention/deletion rules should be defined before launch.

## Security
Use HTTPS, server-side secrets, password hashing through a dedicated identity provider or modern password hashing library, rate limits, input validation, CORS allowlists, audit logging, and strict authorization. Never commit API keys or passwords.

## Project integration
Each project exposes `social/agents.json` describing its specialist agent, assistant, and topic bot. The central service remains the source of truth for profiles and cross-project conversations.
