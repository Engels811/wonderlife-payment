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

@app.route("/api/panel/stats/overview", methods=["GET"])
def stats_overview():
    require_panel_auth()

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT
            COUNT(*) AS total_payments,
            SUM(amount) AS total_revenue
        FROM payments
        WHERE status='paid'
    """)
    total = cur.fetchone()

    cur.execute("""
        SELECT provider, COUNT(*) AS count, SUM(amount) AS revenue
        FROM payments
        WHERE status='paid'
        GROUP BY provider
    """)
    by_provider = cur.fetchall()

    cur.close()
    db.close()

    return jsonify({
        "total_payments": total["total_payments"] or 0,
        "total_revenue_cents": total["total_revenue"] or 0,
        "by_provider": by_provider
    })


@app.route("/api/panel/stats/range", methods=["GET"])
def stats_range():
    require_panel_auth()

    start = request.args.get("start")  # YYYY-MM-DD
    end = request.args.get("end")      # YYYY-MM-DD

    if not start or not end:
        return jsonify({"error": "start and end required"}), 400

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT
            DATE(created_at) AS day,
            COUNT(*) AS payments,
            SUM(amount) AS revenue
        FROM payments
        WHERE status='paid'
          AND DATE(created_at) BETWEEN %s AND %s
        GROUP BY day
        ORDER BY day ASC
    """, (start, end))

    rows = cur.fetchall()
    cur.close()
    db.close()

    return jsonify(rows)
