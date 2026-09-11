# KI Social Layer

Shared foundation for all KI projects: profiles, user-to-user conversations and separate topic agents.

## Conversation types
- `user`: user-to-user chat
- `agent`: user ↔ specialist KI agent
- `assistant`: user ↔ general assistant
- `bot`: automated topic bot

## Architecture
Each project keeps its own UI/topic configuration while the Social Layer provides a common API contract. Production deployment should add authentication, HTTPS, PostgreSQL, rate limiting, WebSocket/SSE realtime delivery and encrypted secrets.

## API
- `GET /api/health`
- `POST /api/profiles`
- `GET /api/profiles/<username>`
- `POST /api/chats`
- `POST /api/chats/<id>/messages`
- `GET /api/chats/<id>/messages`
