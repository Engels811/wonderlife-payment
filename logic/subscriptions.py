from datetime import datetime, timedelta
import mysql.connector, os

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

def create_subscription(
    discord_id: int,
    product: str,
    role_id: int,
    days: int,
    provider: str,
    price_cents: int,
    auto_renew: bool
):
    start = datetime.utcnow()
    end = start + timedelta(days=days)

    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO subscriptions
        (discord_id, product, role_id, start_date, end_date,
         auto_renew, payment_provider, price_cents, billing_interval_days)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            discord_id,
            product,
            role_id,
            start,
            end,
            auto_renew,
            provider,
            price_cents,
            days
        )
    )

    cur.close()
    db.close()

def get_expired_auto_renew_subscriptions():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        """
        SELECT *
        FROM subscriptions
        WHERE auto_renew=1
          AND active=1
          AND end_date <= UTC_TIMESTAMP()
        """
    )

    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows

def extend_subscription(sub_id: int, days: int):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        UPDATE subscriptions
        SET
            start_date = end_date,
            end_date = DATE_ADD(end_date, INTERVAL %s DAY),
            last_renewed = UTC_TIMESTAMP()
        WHERE id=%s
        """,
        (days, sub_id)
    )

    cur.close()
    db.close()

def disable_subscription(sub_id: int):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "UPDATE subscriptions SET active=0 WHERE id=%s",
        (sub_id,)
    )

    cur.close()
    db.close()
