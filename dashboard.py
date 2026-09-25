
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time

DB_PATH = "database/smart_grid.db"

# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="Smart Grid Edge Monitor",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Smart Grid Edge Monitoring System")
st.caption("Local Power Consumption Monitoring & Edge Anomaly Detection")

# --------------------------------
# Load database
# --------------------------------

def load_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT *
        FROM power_data
        ORDER BY timestamp
        """,
        conn
    )

    conn.close()

    return df


# --------------------------------
# Load data
# --------------------------------

df = load_data()

# --------------------------------
# Check database
# --------------------------------

if df.empty:

    st.warning(
        "Waiting for power data..."
    )

    st.stop()


# --------------------------------
# Convert timestamp
# --------------------------------

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="mixed"
)

# --------------------------------
# Calculate metrics
# --------------------------------

current_power = df["power"].iloc[-1]

total_energy = df["energy"].sum()

anomaly_count = (
    df["status"] == "ANOMALY"
).sum()

normal_count = (
    df["status"] == "NORMAL"
).sum()


# --------------------------------
# Status
# --------------------------------

latest_status = df["status"].iloc[-1]


# --------------------------------
# Dashboard metrics
# --------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "⚡ Current Power",
    f"{current_power:.2f} W"
)

col2.metric(
    "🔋 Energy",
    f"{total_energy:.3f} kWh"
)

col3.metric(
    "⚠️ Anomalies",
    anomaly_count
)

col4.metric(
    "📊 Total Readings",
    len(df)
)


st.divider()


# --------------------------------
# System status
# --------------------------------

if latest_status == "ANOMALY":

    st.error(
        f"⚠️ ANOMALY DETECTED — "
        f"Current Power: {current_power:.2f} W"
    )

else:

    st.success(
        f"🟢 SYSTEM NORMAL — "
        f"Current Power: {current_power:.2f} W"
    )


# --------------------------------
# Power graph
# --------------------------------

st.subheader("📈 Live Power Consumption")

# Show latest 100 readings
plot_df = df.tail(100)

fig = px.line(
    plot_df,
    x="timestamp",
    y="power",
    markers=True,
    title="Power Consumption"
)

# Highlight anomalies
anomalies = plot_df[
    plot_df["status"] == "ANOMALY"
]

if not anomalies.empty:

    fig.add_scatter(
        x=anomalies["timestamp"],
        y=anomalies["power"],
        mode="markers",
        name="Anomaly",
        marker=dict(
            size=12,
            symbol="x"
        )
    )

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Power (W)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------
# Latest readings
# --------------------------------

st.subheader("📋 Latest Power Readings")

latest = df.tail(10).copy()

st.dataframe(
    latest[
        [
            "timestamp",
            "voltage",
            "current",
            "power",
            "status"
        ]
    ].sort_values(
        "timestamp",
        ascending=False
    ),
    use_container_width=True
)


# --------------------------------
# Anomaly table
# --------------------------------

st.subheader("🚨 Detected Anomalies")

anomaly_df = df[
    df["status"] == "ANOMALY"
].tail(10)

if not anomaly_df.empty:

    st.dataframe(
        anomaly_df[
            [
                "timestamp",
                "voltage",
                "current",
                "power",
                "status"
            ]
        ].sort_values(
            "timestamp",
            ascending=False
        ),
        use_container_width=True
    )

else:

    st.info(
        "No anomalies detected yet."
    )


# --------------------------------
# Edge information
# --------------------------------

st.divider()

st.subheader("🖥️ Edge Computing Status")

c1, c2, c3 = st.columns(3)

c1.success(
    "Edge Processing: ACTIVE"
)

c2.success(
    "Local Database: ACTIVE"
)

c3.info(
    "Cloud Dependency: NONE"
)

# --------------------------------
# Model Optimization
# --------------------------------

st.divider()

st.subheader("🧠 Edge Model Optimization")

original_size = 1260.21
compressed_size = 324.26
reduction = 74.27

col1, col2, col3 = st.columns(3)

col1.metric(
    "Original Model",
    f"{original_size:.2f} KB"
)

col2.metric(
    "Compressed Model",
    f"{compressed_size:.2f} KB",
    delta=f"-{reduction:.2f}%"
)

col3.metric(
    "Storage Reduction",
    f"{reduction:.2f}%"
)

st.progress(
    reduction / 100
)

st.info(
    "The Isolation Forest model was compressed using Joblib "
    "compression level 9. Model size was reduced from "
    "1260.21 KB to 324.26 KB, achieving a 74.27% reduction."
)
# --------------------------------
# Auto refresh
# --------------------------------

time.sleep(2)

st.rerun()
