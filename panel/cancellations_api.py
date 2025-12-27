from flask import Flask, request, jsonify
from panel.auth import require_panel_auth
from logic.cancellations import cancel_subscription

app = Flask(__name__)

@app.route("/api/panel/subscriptions/<int:sub_id>/cancel", methods=["POST"])
def cancel(sub_id):
    require_panel_auth()
    cancel_subscription(sub_id, by="admin")
    return jsonify({"status": "cancelled"})
