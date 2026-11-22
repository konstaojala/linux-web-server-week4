
from flask import Flask
from pathlib import Path
import pymysql

app = Flask(__name__)


def get_visit_count():
    password_file = Path.home() / ".config/week4-reader/mariadb-password"
    password = password_file.read_text().rstrip("\r\n")

    connection = pymysql.connect(
        unix_socket="/run/mysqld/mysqld.sock",
        user="week4_reader",
        password=password,
        database="week4_counter"
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT visit_count FROM visits WHERE id = 1"
            )
            result = cursor.fetchone()

            if result is None:
                raise RuntimeError("Visitor counter not found")

            return result[0]
    finally:
        connection.close()


@app.route("/viikko4/")
@app.route("/week4/")
def home():
    visits = get_visit_count()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Week 4 - Replicated visitor counter</title>
        <style>
            body {{
                background: #111;
                color: #eee;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 60px 20px;
            }}
            h1 {{ color: #d4af37; }}
            .count {{
                color: #75d68b;
                font-size: 64px;
                font-weight: bold;
                margin: 30px;
            }}
            a {{ color: #75d68b; }}
        </style>
    </head>
    <body>
        <h1>Week 4 - server b</h1>
        <h2>Replicated visitor counter</h2>

        <p>Visitor count from server a:</p>
        <div class="count">{visits}</div>

        <p>This is a read only replica.</p>
        <p>Refreshing this page does not increase the count.</p>

        <p>
            <a href="http://193.166.24.178/week2/">
                Visit server a counter
            </a>
        </p>
    </body>
    </html>
    """
