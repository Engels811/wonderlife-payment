import mysql.connector, os
from datetime import datetime

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

def cancel_subscription(sub_id, by="user"):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "UPDATE subscriptions SET auto_renew=0 WHERE id=%s",
        (sub_id,)
    )

    cur.execute(
        """
        INSERT INTO cancellations
        (subscription_id, cancelled_at, cancelled_by)
        VALUES (%s,%s,%s)
        """,
        (sub_id, datetime.utcnow(), by)
    )

    cur.close()
    db.close()
