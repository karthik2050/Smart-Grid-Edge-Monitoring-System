import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

data = []

start_time = datetime.now()

for i in range(1000):

    timestamp = start_time + timedelta(seconds=i)

    # Normal voltage
    voltage = np.random.normal(230, 2)

    # Normal current
    current = np.random.normal(3, 0.5)

    # Calculate power
    power = voltage * current

    # Add artificial anomalies
    if i in [200, 450, 700, 850]:
        current = np.random.uniform(15, 20)
        power = voltage * current

    # Energy in kWh for 1 second
    energy = power / 1000 / 3600

    data.append([
        timestamp,
        voltage,
        current,
        power,
        energy
    ])

df = pd.DataFrame(
    data,
    columns=[
        "timestamp",
        "voltage",
        "current",
        "power",
        "energy"
    ]
)

df.to_csv("data/power_data.csv", index=False)

print("Smart meter simulation completed.")
print("Data saved to data/power_data.csv")
print()
print(df.head())
