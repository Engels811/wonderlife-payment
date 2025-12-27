from flask import Flask, jsonify
from panel.auth import require_panel_auth
import mysql.connector, os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

@app.route("/api/panel/bundles", methods=["GET"])
def list_bundles():
    require_panel_auth()
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM product_bundles")
    rows = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(rows)
