import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load smart meter data
df = pd.read_csv("data/power_data.csv")

# Features used by the ML model
X = df[["voltage", "current", "power"]]

# Create Isolation Forest model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# Train model
model.fit(X)

# Predict anomalies
df["prediction"] = model.predict(X)

# Convert prediction into readable status
df["status"] = df["prediction"].apply(
    lambda x: "ANOMALY" if x == -1 else "NORMAL"
)

# Save trained model
joblib.dump(model, "models/anomaly_model.pkl")

# Save results
df.to_csv("data/detected_data.csv", index=False)

# Display results
print("\nAnomaly Detection Completed")
print("--------------------------------")

print("Total readings:", len(df))
print("Normal readings:", (df["status"] == "NORMAL").sum())
print("Anomalies:", (df["status"] == "ANOMALY").sum())

print("\nDetected Anomalies:")
print(
    df[df["status"] == "ANOMALY"][
        ["timestamp", "voltage", "current", "power", "status"]
    ]
)

