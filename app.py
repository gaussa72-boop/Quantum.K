from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

PAGE = '''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quantum.K</title><style>body{margin:0;background:#050711;color:#eef5ff;font:16px system-ui;text-align:center}main{max-width:900px;margin:auto;padding:12vh 24px}.core{margin:40px auto;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,#fff,#8fd7ff 12%,#675cff 35%,transparent 70%);box-shadow:0 0 90px #635cff}h1{font-size:48px}p{color:#aab7d4}button{padding:12px 18px;border-radius:10px;border:0;font-weight:700}</style></head><body><main><div class="core"></div><h1>QUANTUM.K</h1><p>Eigenständige Quantum-Core-App · sichere Rechenmodelle · API</p><button onclick="fetch('/api/health').then(r=>r.json()).then(x=>alert(JSON.stringify(x)))">CORE STATUS</button></main></body></html>'''

@app.get('/')
def index(): return render_template_string(PAGE)

@app.get('/api/health')
def health(): return jsonify(status='ok', app='Quantum.K', mode='standalone')

if __name__ == '__main__': app.run(host='127.0.0.1', port=5001, debug=False)
