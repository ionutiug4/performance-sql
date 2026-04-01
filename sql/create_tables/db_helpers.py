import psycopg2
from psycopg2 import sql
import constants


def connect():
    return psycopg2.connect(**constants.DEFAULT_CONN_PARAMS)


def createUsersTable():
    conn = None

    try:
        conn = connect()
        conn.autocommit = True

        with conn.cursor() as cursor:
            create_table_query = sql.SQL(
                f"""
                CREATE TABLE IF NOT EXISTS {constants.ACTIVE_USERS_TABLE} (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    available BOOLEAN NOT NULL
                    )"""
            )
            cursor.execute(create_table_query)
            print("Table 'active_users' checked/created successfully")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
