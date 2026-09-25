import pandas as pd
import numpy as np
import sqlite3
import joblib
import time
from datetime import datetime
from sklearn.ensemble import IsolationForest

DB_PATH = "database/smart_grid.db"


# -----------------------------
# Create database
# -----------------------------
def create_database():

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
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


# -----------------------------
# Generate power reading
# -----------------------------
def generate_reading():

    voltage = np.random.normal(230, 2)

    current = np.random.normal(3, 0.5)

    # Occasionally create abnormal consumption
    if np.random.random() < 0.05:
        current = np.random.uniform(15, 20)

    power = voltage * current

    energy = power / 1000 / 3600

    return voltage, current, power, energy


# -----------------------------
# Train anomaly model
# -----------------------------
def train_model():

    normal_power = np.random.normal(700, 120, 1000)

    normal_voltage = np.random.normal(230, 2, 1000)

    normal_current = normal_power / normal_voltage

    X = pd.DataFrame({
        "voltage": normal_voltage,
        "current": normal_current,
        "power": normal_power
    })

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    joblib.dump(
        model,
        "models/anomaly_model.pkl"
    )

    return model


# -----------------------------
# Store reading
# -----------------------------
def store_reading(
    timestamp,
    voltage,
    current,
    power,
    energy,
    status
):

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO power_data
        (timestamp, voltage, current, power, energy, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        voltage,
        current,
        power,
        energy,
        status
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Main Edge Application
# -----------------------------
def main():

    print("=" * 50)
    print(" SMART GRID EDGE APPLICATION")
    print("=" * 50)

    create_database()

    print("Starting Edge ML model...")

    model = train_model()

    print("Edge model ready.")
    print("Starting power monitoring...")
    print("Press Ctrl+C to stop.\n")

    try:

        while True:

            voltage, current, power, energy = generate_reading()

            data = [[
                voltage,
                current,
                power
            ]]

            prediction = model.predict(data)[0]

            if prediction == -1:
                status = "ANOMALY"
            else:
                status = "NORMAL"

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            store_reading(
                timestamp,
                voltage,
                current,
                power,
                energy,
                status
            )

            if status == "ANOMALY":

                print(
                    f"⚠️ ANOMALY | "
                    f"{timestamp} | "
                    f"Power: {power:.2f} W"
                )

            else:

                print(
                    f"✓ NORMAL  | "
                    f"{timestamp} | "
                    f"Power: {power:.2f} W"
                )

            time.sleep(2)

    except KeyboardInterrupt:

        print("\n")
        print("Edge monitoring stopped.")
        print("Data remains stored locally.")


if __name__ == "__main__":
    main()

