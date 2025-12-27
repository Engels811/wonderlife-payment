import mysql.connector, os

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True
    )

def get_bundle_roles(product_name):
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        """
        SELECT pb.role_id
        FROM bundle_items bi
        JOIN product_bundles pb ON pb.id = bi.bundle_id
        WHERE bi.product_name=%s
        """,
        (product_name,)
    )

    roles = [r["role_id"] for r in cur.fetchall()]
    cur.close()
    db.close()
    return roles
