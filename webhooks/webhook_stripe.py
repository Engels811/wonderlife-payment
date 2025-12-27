from flask import Flask, request, abort
import os
import stripe
import mysql.connector
from datetime import datetime

# ============================================
# APP SETUP
# ============================================

app = Flask(__name__)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

if not STRIPE_SECRET_KEY or not STRIPE_WEBHOOK_SECRET:
    raise RuntimeError("Stripe ENV variables are missing")

stripe.api_key = STRIPE_SECRET_KEY

# ============================================
# DATABASE
# ============================================

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )

# ============================================
# WEBHOOK ENDPOINT
# ============================================

@app.route("/webhooks/stripe", methods=["POST"])
def stripe_webhook():

    payload = request.data
    sig_header = request.headersget = request.headers.get("Stripe-Signature")

    if not sig_header:
        abort(400, "Missing Stripe signature")

    # ----------------------------------------
    # VERIFY SIGNATURE
    # ----------------------------------------
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        abort(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        abort(400, "Invalid Stripe signature")

    # ----------------------------------------
    # FILTER EVENTS
    # ----------------------------------------
    if event["type"] != "checkout.session.completed":
        return "", 200

    session = event["data"]["object"]
    event_id = event["id"]
    session_id = session["id"]

    # ----------------------------------------
    # VALIDATE METADATA
    # ----------------------------------------
    metadata = session.get("metadata", {})

    if "discord_id" not in metadata or "product" not in metadata:
        abort(400, "Missing required metadata")

    try:
        discord_id = int(metadata["discord_id"])
    except ValueError:
        abort(400, "discord_id is not valid")

    product_name = metadata["product"]
    amount_cents = session.get("amount_total", 0)

    # ----------------------------------------
    # DUPLICATE PROTECTION (EVENT-BASED)
    # ----------------------------------------
    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        SELECT id FROM payments
        WHERE provider='stripe'
          AND external_id=%s
        """,
        (event_id,)
    )

    if cur.fetchone():
        cur.close()
        db.close()
        return "", 200

    # ----------------------------------------
    # STORE PAYMENT
    # ----------------------------------------
    cur.execute(
        """
        INSERT INTO payments
        (discord_id, provider, product, amount, status, external_id, created_at)
        VALUES (%s, 'stripe', %s, %s, 'paid', %s, %s)
        """,
        (
            discord_id,
            product_name,
            amount_cents,
            event_id,
            datetime.utcnow()
        )
    )

    db.commit()
    cur.close()
    db.close()

    print(
        f"[STRIPE] OK | Event {event_id} | "
        f"Discord {discord_id} | {product_name} | "
        f"{amount_cents / 100:.2f}€"
    )

    return "", 200


# ============================================
# LOCAL START (DEV ONLY)
# ============================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
