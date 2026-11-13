from flask import Flask, jsonify, render_template_string, request
import os
import requests

app = Flask(__name__)

# SECURITY HARDENING
from collections import defaultdict, deque
from time import monotonic
_SEC_RATE=defaultdict(deque)
@app.before_request
def _sec_before():
    if request.content_length and request.content_length > 1048576:return jsonify(error="Request too large."),413
    if request.path.startswith("/.git/") or request.path.startswith("/.env"):return jsonify(error="Not Found."),404
    q=_SEC_RATE[request.remote_addr or "unknown"];now=monotonic()
    while q and now-q[0]>60:q.popleft()
    if len(q)>=(30 if request.method=="POST" else 120):return jsonify(error="Too many requests."),429
    q.append(now)
@app.after_request
def _sec_headers(response):
    response.headers["X-Content-Type-Options"]="nosniff";response.headers["X-Frame-Options"]="DENY";response.headers["Referrer-Policy"]="strict-origin-when-cross-origin";response.headers["Permissions-Policy"]="camera=(), microphone=(), geolocation=()";response.headers["Strict-Transport-Security"]="max-age=31536000; includeSubDomains";response.headers.pop("Server",None);return response


# --- Security hardening ---
from collections import defaultdict, deque
from time import monotonic
from html import escape as html_escape

_SECURITY_RATE = defaultdict(deque)
_SECURITY_WINDOW = 60
_SECURITY_MAX = 120
_SECURITY_POST_MAX = 30
_SECURITY_MAX_BODY = 1024 * 1024

@app.before_request
def _security_before_request():
    if request.content_length and request.content_length > _SECURITY_MAX_BODY:
        return jsonify(error="Request too large."), 413
    path = request.path or "/"
    blocked = {"/.env","/.git/config","/server.py","/app.py","/main.py","/package.json","/requirements.txt","/render.yaml","/Procfile"}
    if path in blocked or path.startswith("/.git/") or path.startswith("/.env"):
        return jsonify(error="Not Found."), 404
    ip = request.remote_addr or "unknown"
    now = monotonic()
    q = _SECURITY_RATE[ip]
    while q and now - q[0] > _SECURITY_WINDOW:
        q.popleft()
    limit = _SECURITY_POST_MAX if request.method in {"POST","PUT","PATCH","DELETE"} else _SECURITY_MAX
    if len(q) >= limit:
        return jsonify(error="Too many requests. Please try again later."), 429
    q.append(now)

@app.after_request
def _security_headers(response):
    response.headers.setdefault("X-Content-Type-Options","nosniff")
    response.headers.setdefault("X-Frame-Options","DENY")
    response.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy","camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("Cross-Origin-Opener-Policy","same-origin")
    response.headers.setdefault("Strict-Transport-Security","max-age=31536000; includeSubDomains")
    response.headers.setdefault("Cache-Control","no-store" if request.path.startswith("/api/") else "public, max-age=300")
    response.headers.pop("Server", None)
    return response
# --- End security hardening ---

PAGE = '''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quantum Super Intelligence</title>
<style>
:root{color-scheme:dark;--bg:#070914;--panel:#111629;--line:rgba(255,255,255,.12);--cyan:#8be7f3;--muted:#9da9c2}
*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 50% -15%,#32205f 0,transparent 55%),var(--bg);color:#f2f4ff;font:15px system-ui}
header{height:70px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 22px;background:#080b18d9;backdrop-filter:blur(16px)}
.brand{display:flex;gap:12px;align-items:center;font-weight:800;letter-spacing:.09em}.core{width:32px;height:32px;border-radius:50%;background:radial-gradient(circle,#fff,#8be7f3 18%,#7357ff 55%,transparent 72%);box-shadow:0 0 26px #7357ff}
.status{font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:7px 12px}
main{max-width:940px;margin:auto;padding:34px 18px;min-height:calc(100vh - 70px);display:flex;flex-direction:column}
h1{font-size:clamp(26px,5vw,44px);margin:12px 0 6px}.sub{color:var(--muted);margin:0 0 22px}
#messages{flex:1;min-height:260px;max-height:62vh;overflow:auto;display:flex;flex-direction:column;gap:14px;padding:14px 0}
.msg{max-width:88%;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.55;padding:13px 16px;border:1px solid var(--line);border-radius:16px;background:var(--panel)}
.msg.user{align-self:flex-end;background:#1d1d42;border-color:#443c83}.msg.ai{align-self:flex-start}
form{display:flex;gap:10px;align-items:flex-end;border:1px solid var(--line);border-radius:18px;background:#111629;padding:10px}
textarea{flex:1;min-height:54px;max-height:180px;resize:vertical;background:transparent;color:#fff;border:0;outline:0;padding:10px;font:inherit}
button{border:0;border-radius:12px;padding:12px 18px;background:linear-gradient(135deg,#9b78ff,#62d4df);color:#0b0d1b;font-weight:800;cursor:pointer}button:disabled{opacity:.55;cursor:wait}
.note{font-size:12px;color:var(--muted);margin:10px 4px}
@media(max-width:600px){header{padding:0 13px}main{padding:22px 12px}.msg{max-width:96%}form{gap:5px;padding:8px}button{padding:11px 13px}}
</style></head><body>
<header><div class="brand"><span class="core"></span><span>QUANTUM SUPER INTELLIGENCE</span></div><div id="status" class="status">KI wird geprüft …</div></header>
<main><h1>Denke weiter.</h1><p class="sub">Ein zentraler KI-Arbeitsraum für Analyse, Wissen, Ideen und Code.</p>
<div id="messages" aria-live="polite"><div class="msg ai">Willkommen. Ich bin Quantum Super Intelligence. Was möchtest du entwickeln oder verstehen?</div></div>
<form id="form"><textarea id="message" placeholder="Nachricht an Quantum Super Intelligence …" required></textarea><button id="send" type="submit">Senden</button></form>
<p class="note">Für echte KI-Antworten muss OPENAI_API_KEY in Render hinterlegt sein. Schlüssel bleiben serverseitig.</p></main>
<script>
const messages=document.getElementById('messages'),statusEl=document.getElementById('status'),form=document.getElementById('form'),input=document.getElementById('message'),send=document.getElementById('send');
function add(role,text){const e=document.createElement('div');e.className='msg '+role;e.textContent=text;messages.appendChild(e);messages.scrollTop=messages.scrollHeight}
async function health(){try{const r=await fetch('/api/health',{cache:'no-store'}),x=await r.json();statusEl.textContent=x.ai_configured?'● Verbunden · '+x.model:'○ API-Key fehlt';statusEl.style.color=x.ai_configured?'#8de5b1':'#f2c27a'}catch(_){statusEl.textContent='Status nicht verfügbar'}}
form.addEventListener('submit',async e=>{e.preventDefault();const message=input.value.trim();if(!message)return;add('user',message);input.value='';send.disabled=true;send.textContent='…';try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})}),d=await r.json();if(!r.ok)throw new Error(d.error||('HTTP '+r.status));add('ai',d.reply||'Keine Antwort erhalten.')}catch(err){add('ai','Fehler: '+err.message)}finally{send.disabled=false;send.textContent='Senden';input.focus()}});
input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();form.requestSubmit()}});
health();
</script><script src="https://ultima-membership-api.onrender.com/support-widget.js" defer></script></body></html>'''

@app.get('/')
def index(): return render_template_string(PAGE)

@app.get('/api/health')
def health(): return jsonify(status='ok', app='Quantum.K', mode='openai-chat', ai_configured=bool(os.getenv('OPENAI_API_KEY','').strip()), model=os.getenv('OPENAI_MODEL','gpt-4o-mini'))

if __name__ == '__main__': app.run(host='127.0.0.1', port=5001, debug=False)
