from flask import Flask, jsonify, render_template_string

app = Flask(__name__)


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

PAGE = '''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quantum.K</title><style>body{margin:0;background:#050711;color:#eef5ff;font:16px system-ui;text-align:center}main{max-width:900px;margin:auto;padding:12vh 24px}.core{margin:40px auto;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,#fff,#8fd7ff 12%,#675cff 35%,transparent 70%);box-shadow:0 0 90px #635cff}h1{font-size:48px}p{color:#aab7d4}button{padding:12px 18px;border-radius:10px;border:0;font-weight:700}</style></head><body><main><div class="core"></div><h1>QUANTUM.K</h1><p>Eigenständige Quantum-Core-App · sichere Rechenmodelle · API</p><button onclick="fetch('/api/health').then(r=>r.json()).then(x=>alert(JSON.stringify(x)))">CORE STATUS</button></main></body></html>'''

@app.get('/')
def index(): return render_template_string(PAGE)

@app.get('/api/health')
def health(): return jsonify(status='ok', app='Quantum.K', mode='standalone')

if __name__ == '__main__': app.run(host='127.0.0.1', port=5001, debug=False)
