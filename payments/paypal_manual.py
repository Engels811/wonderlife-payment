from db import get_db
from datetime import datetime

def register_paypal_payment(discord_id, product, amount_cents):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """INSERT INTO payments
        (discord_id, provider, product, amount, status, created_at)
        VALUES (%s,'paypal',%s,%s,'paid',%s)""",
        (discord_id, product, amount_cents, datetime.utcnow())
    )
    db.commit()
    cur.close()
    db.close()
