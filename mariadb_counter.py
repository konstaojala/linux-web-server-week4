
import pymysql
from pathlib import Path


def get_visit_count():
    password_file = Path.home() / ".config/viikko2/mariadb-password"
    password = password_file.read_text().rstrip("\n")

    connection = pymysql.connect(
        unix_socket="/run/mysqld/mysqld.sock",
        user="week2_app",
        password=password,
        database="week4_counter"
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE visits SET visit_count = visit_count + 1 WHERE id = 1"
            )

            if cursor.rowcount != 1:
                raise RuntimeError("Visitor counter row is missing")

            cursor.execute(
                "SELECT visit_count FROM visits WHERE id = 1"
            )

            count = cursor.fetchone()[0]

        connection.commit()
        return count

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
