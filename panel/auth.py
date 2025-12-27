import os
from flask import request, abort

PANEL_API_TOKEN = os.getenv("PANEL_API_TOKEN")

if not PANEL_API_TOKEN:
    raise RuntimeError("❌ PANEL_API_TOKEN is not set")

def require_panel_auth():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {PANEL_API_TOKEN}":
        abort(401, "Unauthorized")
