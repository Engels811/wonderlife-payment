from flask import Flask, jsonify, send_file, abort, request
import os
import mysql.connector
from panel.auth import require_panel_auth
from panel.utils import safe_invoice_path

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

# ============================================
# LISTE ALLER RECHNUNGEN
# ============================================

@app.route("/api/panel/invoices", methods=["GET"])
def list_invoices():
    require_panel_auth()

    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        """
        SELECT
            id,
            discord_id,
            provider,
            product,
            amount,
            invoice_number,
            created_at
        FROM payments
        WHERE invoice_number IS NOT NULL
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """,
        (limit, offset)
    )

    rows = cur.fetchall()
    cur.close()
    db.close()

    return jsonify({
        "count": len(rows),
        "data": rows
    })

# ============================================
# EINZELNE RECHNUNG (PDF)
# ============================================

@app.route("/api/panel/invoices/<invoice_number>", methods=["GET"])
def download_invoice(invoice_number: str):
    require_panel_auth()

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        """
        SELECT invoice_pdf
        FROM payments
        WHERE invoice_number=%s
        """,
        (invoice_number,)
    )

    row = cur.fetchone()
    cur.close()
    db.close()

    if not row or not row["invoice_pdf"]:
        abort(404, "Invoice not found")

    path = safe_invoice_path(row["invoice_pdf"])
    if not path:
        abort(403, "Invalid invoice path")

    return send_file(
        path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"{invoice_number}.pdf"
    )
