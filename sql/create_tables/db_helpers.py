import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import constants

load_dotenv()


def get_db_params(admin: bool):
    db_name = (
        os.getenv("POSTGRES_DATABASE") if admin else os.getenv("POSTGRES_SPEEDRUN")
    )
    return {
        "database": db_name,
        "host": os.getenv("POSTGRES_HOST"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "port": int(os.getenv("POSTGRES_PORT", 5432)),
    }


def connect(value: bool):
    params = get_db_params(value)
    return psycopg2.connect(**params)


def create_speedrun_database():
    conn = None

    try:
        conn = connect(True)
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'speedrun'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier("speedrun"))
                )
                print("Speedrun database created successfully!")
            else:
                print("Database 'speedrun' already exists.")

    except Exception as e:
        print(f"Error creating speedrun database: {e}")
    finally:
        if conn:
            conn.close()


def create_users_table():
    conn = None

    try:
        conn = connect(False)
        conn.autocommit = True

        with conn.cursor() as cursor:
            create_table_query = sql.SQL(
                f"""
                CREATE TABLE IF NOT EXISTS {constants.ACTIVE_USERS_TABLE} (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email_address VARCHAR(50) NOT NULL UNIQUE,
                    is_available BOOLEAN NOT NULL
                    )"""
            )
            cursor.execute(create_table_query)
            print(
                f"Table '{constants.ACTIVE_USERS_TABLE}' checked/created successfully"
            )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()


def create_user(
    first_name: str, last_name: str, email_address: str, is_available: bool
):
    conn = None

    try:
        conn = connect(False)
        conn.autocommit = True

        with conn.cursor() as cursor:
            create_user_query = sql.SQL(
                """
            INSERT INTO {table} (first_name, last_name, email_address, is_available)
            VALUES (%s, %s, %s, %s)
            """
            ).format(table=sql.Identifier(constants.ACTIVE_USERS_TABLE))

            cursor.execute(
                create_user_query, (first_name, last_name, email_address, is_available)
            )
            print(f"User with email address {email_address} created successfully")

    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        if conn:
            conn.close()
