import os
import joblib

input_file = "models/anomaly_model.pkl"
output_file = "models/anomaly_model_compressed.pkl"

# Load model
model = joblib.load(input_file)

# Save with maximum compression
joblib.dump(
    model,
    output_file,
    compress=9
)

# Check file sizes
original_size = os.path.getsize(input_file)
compressed_size = os.path.getsize(output_file)

print("Original size   :", round(original_size / 1024, 2), "KB")
print("Compressed size :", round(compressed_size / 1024, 2), "KB")

reduction = (1 - compressed_size / original_size) * 100

print("Size reduction  :", round(reduction, 2), "%")
