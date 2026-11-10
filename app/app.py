import os

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


@app.route("/")
def index():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM items ORDER BY id")
            items = cursor.fetchall()
    finally:
        connection.close()

    html = "<h1>Items from PostgreSQL</h1><ul>"

    for item in items:
        html += f"<li>{item[0]}: {item[1]}</li>"

    html += "</ul>"

    return html


@app.route("/api/items")
def api_items():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM items ORDER BY id")
            items = cursor.fetchall()
    finally:
        connection.close()

    return jsonify([
        {"id": item[0], "name": item[1]}
        for item in items
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", "5000")))
