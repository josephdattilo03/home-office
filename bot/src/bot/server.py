import os
import json
import subprocess
import threading
import hmac
from urllib.request import Request, urlopen
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MM_URL = os.environ.get("MM_URL", "http://mattermost:8065")
WEBHOOK_TOKEN = os.environ["MM_WEBHOOK_TOKEN"]
BOT_TOKEN = os.environ["MM_BOT_TOKEN"]
CLAUDE = ["claude", "-p", "--model", "haiku", "--tools", "", "--no-session-persistence"]


def mm(method, path, body=None):
    req = Request(
        f"{MM_URL}/api/v4{path}",
        method=method,
        data=json.dumps(body).encode() if body else None,
        headers={
            "Authorization": f"Bearer {BOT_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urlopen(req, timeout=10) as r:
        return json.load(r)


def ask_claude(prompt):
    try:
        r = subprocess.run(
            CLAUDE, input=prompt, capture_output=True, text=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        return "Timed out."
    return (
        r.stdout.strip()
        if r.returncode == 0
        else f"claude failed: {r.stderr.strip()[:500]}"
    )


def handle(p):
    prompt = p["text"].removeprefix(p["trigger_word"]).strip()
    post = mm("GET", f"/posts/{p['post_id']}")
    ans = ask_claude(prompt) if prompt else "Usage: @bot <prompt>"
    mm(
        "POST",
        "/posts",
        {
            "channel_id": p["channel_id"],
            "root_id": post["root_id"] or post["id"],
            "message": ans,
        },
    )


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        p = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if not hmac.compare_digest(p.get("token", ""), WEBHOOK_TOKEN):
            self.send_response(403)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b"{}")
        threading.Thread(target=handle, args=(p,), daemon=True).start()


def main() -> None:
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
