from flask import Flask, jsonify, request
import os
import mysql.connector
from panel.auth import require_panel_auth

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

@app.route("/api/panel/payments", methods=["GET"])
def list_payments():
    require_panel_auth()

    provider = request.args.get("provider")   # stripe | tebex | paypal | psc
    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))

    db = get_db()
    cur = db.cursor(dictionary=True)

    sql = "SELECT * FROM payments"
    params = []

    if provider:
        sql += " WHERE provider=%s"
        params.append(provider)

    sql += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cur.execute(sql, params)
    rows = cur.fetchall()

    cur.close()
    db.close()

    return jsonify({
        "count": len(rows),
        "data": rows
    })
