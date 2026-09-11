-- Quantum.KI Social Layer
CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, username TEXT UNIQUE NOT NULL, display_name TEXT NOT NULL, avatar_url TEXT, bio TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS conversations (id TEXT PRIMARY KEY, kind TEXT NOT NULL, topic TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS conversation_members (conversation_id TEXT NOT NULL, user_id TEXT NOT NULL, PRIMARY KEY (conversation_id,user_id));
CREATE TABLE IF NOT EXISTS messages (id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL, sender_type TEXT NOT NULL, sender_id TEXT, body TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS agents (id TEXT PRIMARY KEY, name TEXT NOT NULL, topic TEXT NOT NULL, system_prompt TEXT NOT NULL, avatar_url TEXT);
