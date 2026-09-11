"""Shared profile + user chat + topic-agent API foundation."""
from datetime import datetime, timezone
from flask import Flask, jsonify, request
import sqlite3, uuid

app = Flask(__name__)
DB = "social.db"

def now(): return datetime.now(timezone.utc).isoformat()
def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init():
    con = db()
    con.executescript(open("social/backend/schema.sql", encoding="utf-8").read())
    con.commit(); con.close()

@app.get("/api/health")
def health(): return jsonify(ok=True, service="KI Social Layer")

@app.post("/api/profiles")
def profile():
    data=request.get_json(force=True)
    uid=data.get("id") or str(uuid.uuid4())
    con=db(); con.execute("INSERT OR REPLACE INTO users VALUES (?,?,?,?,?,?)", (uid,data["username"],data.get("display_name",data["username"]),data.get("avatar_url"),data.get("bio",""),now())); con.commit(); con.close()
    return jsonify(id=uid), 201

@app.get("/api/profiles/<username>")
def get_profile(username):
    row=db().execute("SELECT id,username,display_name,avatar_url,bio,created_at FROM users WHERE username=?",(username,)).fetchone()
    return (jsonify(dict(row)),200) if row else (jsonify(error="profile_not_found"),404)

@app.post("/api/chats")
def create_chat():
    data=request.get_json(force=True); cid=str(uuid.uuid4())
    con=db(); con.execute("INSERT INTO conversations VALUES (?,?,?,?,?)",(cid,data.get("kind","user"),data.get("topic"),now(),));
    for uid in data.get("members",[]): con.execute("INSERT INTO conversation_members VALUES (?,?)",(cid,uid))
    con.commit(); con.close(); return jsonify(id=cid),201

@app.post("/api/chats/<cid>/messages")
def send(cid):
    data=request.get_json(force=True); mid=str(uuid.uuid4())
    con=db(); con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",(mid,cid,data.get("sender_type","user"),data.get("sender_id"),data["body"],now())); con.commit(); con.close()
    return jsonify(id=mid),201

@app.get("/api/chats/<cid>/messages")
def messages(cid):
    rows=db().execute("SELECT * FROM messages WHERE conversation_id=? ORDER BY created_at",(cid,)).fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init(); app.run(host="0.0.0.0",port=5001,debug=True)
