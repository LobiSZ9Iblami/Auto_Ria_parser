import os
import psycopg2
import time
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE,
            title TEXT,
            price_usd INTEGER,
            odometer INTEGER,
            username TEXT,
            phone_number BIGINT,
            image_url TEXT,
            images_count INTEGER,
            car_number TEXT,
            car_vin TEXT,
            datetime_found TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def save_car(car: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cars (
            url,
            title,
            price_usd,
            odometer,
            username,
            phone_number,
            image_url,
            images_count,
            car_number,
            car_vin,
            datetime_found
        )
        VALUES (
            %(url)s,
            %(title)s,
            %(price_usd)s,
            %(odometer)s,
            %(username)s,
            %(phone_number)s,
            %(image_url)s,
            %(images_count)s,
            %(car_number)s,
            %(car_vin)s,
            %(datetime_found)s
        )
        ON CONFLICT (url) DO NOTHING;
    """, car)

    conn.commit()
    cur.close()
    conn.close()

def wait_for_db():
    for _ in range(10):
        try:
            conn = get_connection()
            conn.close()
            print("DB is ready")
            return
        except psycopg2.OperationalError:
            print("Waiting for DB...")
            time.sleep(3)

    raise RuntimeError("DB not ready")
