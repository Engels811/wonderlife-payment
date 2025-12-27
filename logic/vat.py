import mysql.connector, os

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

def calculate_vat(amount_cents: int, country_code: str):
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT vat_rate FROM vat_rates WHERE country_code=%s",
        (country_code.upper(),)
    )
    row = cur.fetchone()
    cur.close()
    db.close()

    vat_rate = row["vat_rate"] if row else 0
    vat_amount = int(amount_cents * vat_rate / 100)

    return {
        "vat_rate": vat_rate,
        "vat_amount": vat_amount,
        "gross": amount_cents + vat_amount
    }
