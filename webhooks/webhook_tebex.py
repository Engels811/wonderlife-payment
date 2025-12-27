from flask import Flask, request, abort
import os
import hmac
import hashlib
import json
import mysql.connector
from datetime import datetime

# ============================================
# APP SETUP
# ============================================

app = Flask(__name__)

TEBEX_SECRET = os.getenv("TEBEX_PRIVATE_KEY")
if not TEBEX_SECRET:
    raise RuntimeError("❌ TEBEX_PRIVATE_KEY is not set")

# ============================================
# DATABASE
# ============================================

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

# ============================================
# SIGNATURE VALIDATION
# ============================================

def verify_tebex_signature(raw_body: bytes, signature: str) -> bool:
    expected = hmac.new(
        TEBEX_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

# ============================================
# WEBHOOK ENDPOINT
# ============================================

@app.route("/webhooks/tebex", methods=["POST"])
def tebex_webhook():

    signature = request.headers.get("X-Tebex-Signature")
    if not signature:
        abort(403, "Missing Tebex signature")

    raw_body = request.get_data()

    if not verify_tebex_signature(raw_body, signature):
        abort(403, "Invalid Tebex signature")

    try:
        data = json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError:
        abort(400, "Invalid JSON")

    # ========================================
    # EVENT FILTER (SEHR WICHTIG)
    # ========================================

    event_type = data.get("type")
    if event_type != "payment.completed":
        # Tebex Test / andere Events ignorieren
        return "", 204

    # ========================================
    # DATA EXTRACTION (GESICHERT)
    # ========================================

    customer = data.get("customer", {})
    if "username" not in customer:
        abort(400, "Missing customer.username (Discord ID)")

    try:
        discord_id = int(customer["username"])
    except ValueError:
        abort(400, "customer.username is not a valid Discord ID")

    package = data.get("package", {})
    payment = data.get("payment", {})

    product_name = package.get("name", "Unknown Product")
    product_id = str(package.get("id", "unknown"))
    amount_eur = float(payment.get("amount", 0))

    amount_cents = int(amount_eur * 100)

    # ========================================
    # DUPLICATE PROTECTION
    # ========================================

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT id FROM payments WHERE provider='tebex' AND product=%s AND discord_id=%s",
        (product_name, discord_id)
    )

    if cur.fetchone():
        # Zahlung wurde bereits verarbeitet
        cur.close()
        db.close()
        return "", 204

    # ========================================
    # STORE PAYMENT
    # ========================================

    cur.execute(
        """
        INSERT INTO payments
        (discord_id, provider, product, amount, status, created_at)
        VALUES (%s, 'tebex', %s, %s, 'paid', %s)
        """,
        (
            discord_id,
            product_name,
            amount_cents,
            datetime.utcnow()
        )
    )

    cur.close()
    db.close()

    # ========================================
    # NÄCHSTE SCHRITTE (HOOKS)
    # ========================================
    # → assign_role(...)
    # → create_payment_ticket(...)
    # → create_invoice(...)
    # → panel sync

    print(
        f"[TEBEX] Zahlung OK | Discord {discord_id} | "
        f"{product_name} | {amount_eur:.2f}€"
    )

    return "", 204


# ============================================
# LOCAL START (DEV ONLY)
# ============================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
