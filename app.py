from flask import Flask, jsonify, render_template_string, request

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

PAGE = '''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quantum.K</title><style>body{margin:0;background:#050711;color:#eef5ff;font:16px system-ui;text-align:center}main{max-width:900px;margin:auto;padding:12vh 24px}.core{margin:40px auto;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,#fff,#8fd7ff 12%,#675cff 35%,transparent 70%);box-shadow:0 0 90px #635cff}h1{font-size:48px}p{color:#aab7d4}button{padding:12px 18px;border-radius:10px;border:0;font-weight:700}<style id="ultima-complete-2026">
:root{color-scheme:dark;--u-cyan:#7de9ef;--u-violet:#9d8bff;--u-line:rgba(166,187,255,.16)}
html{scroll-behavior:smooth}body{overflow-x:hidden!important;background-image:radial-gradient(ellipse at 12% 0%,rgba(101,83,206,.2),transparent 40%),radial-gradient(ellipse at 90% 12%,rgba(31,178,191,.12),transparent 35%)}
header,nav,.sidebar,.side,.panel,.card,.toolbar,.composer{backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}
button,input,textarea,select{font:inherit}input,textarea,select{max-width:100%}
input:focus,textarea:focus,select:focus,button:focus-visible,a:focus-visible{outline:2px solid var(--u-cyan)!important;outline-offset:3px}
button,a{transition:transform .18s ease,box-shadow .18s ease}button:hover{transform:translateY(-1px)}
@media(max-width:760px){.app{height:auto!important;min-height:100vh;display:block!important}.side,.sidebar{width:100%!important;min-height:0!important}.main,.content{width:100%!important;min-width:0!important;padding:14px!important}.grid{display:block!important}.top{flex-wrap:wrap}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation-duration:.01ms!important;transition-duration:.01ms!important}}
</style></style></head><body><main><div class="core"></div><h1>QUANTUM.K</h1><p>Eigenständige Quantum-Core-App · sichere Rechenmodelle · API</p><button onclick="fetch('/api/health').then(r=>r.json()).then(x=>alert(JSON.stringify(x)))">CORE STATUS</button></main></body></html>'''

@app.get('/')
def index(): return render_template_string(PAGE)

@app.get('/api/health')
def health(): return jsonify(status='ok', app='Quantum.K', mode='standalone')

if __name__ == '__main__': app.run(host='127.0.0.1', port=5001, debug=False)
