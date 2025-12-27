import mysql.connector, os
from datetime import datetime, timedelta

MAX_ATTEMPTS = 5

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

def schedule_retry(subscription_id, provider, error):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO payment_retries
        (subscription_id, provider, last_error, next_try)
        VALUES (%s,%s,%s,%s)
        """,
        (
            subscription_id,
            provider,
            error,
            datetime.utcnow() + timedelta(hours=6)
        )
    )

    cur.close()
    db.close()

def process_retries():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        """
        SELECT * FROM payment_retries
        WHERE active=1 AND next_try <= UTC_TIMESTAMP()
        """
    )

    retries = cur.fetchall()

    for r in retries:
        if r["attempt"] >= MAX_ATTEMPTS:
            cur.execute(
                "UPDATE payment_retries SET active=0 WHERE id=%s",
                (r["id"],)
            )
            continue

        # hier später: erneuter Zahlungsversuch (Stripe)
        cur.execute(
            """
            UPDATE payment_retries
            SET attempt=attempt+1,
                next_try=DATE_ADD(UTC_TIMESTAMP(), INTERVAL 6 HOUR)
            WHERE id=%s
            """,
            (r["id"],)
        )

    cur.close()
    db.close()
