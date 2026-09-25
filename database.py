import sqlite3
import pandas as pd

DB_PATH = "database/smart_grid.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS power_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            voltage REAL,
            current REAL,
            power REAL,
            energy REAL,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def store_data():
    df = pd.read_csv("data/detected_data.csv")

    conn = sqlite3.connect(DB_PATH)

    df = df[
        [
            "timestamp",
            "voltage",
            "current",
            "power",
            "energy",
            "status"
        ]
    ]

    df.to_sql(
        "power_data",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()


if __name__ == "__main__":
    create_database()
    store_data()

    print("Database created successfully.")
    print("Power data stored locally.")

