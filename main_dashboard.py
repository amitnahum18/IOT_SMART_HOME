import streamlit as st
import sqlite3
import pandas as pd
import time
from mqtt_init import *

# Page Configuration
st.set_page_config(page_title="Smart Irrigation Dashboard", layout="wide")

st.title("🌱 Smart Irrigation System - Live Monitor")
st.markdown(f"**Monitoring Topic:** `{moisture_topic}`")
st.divider()

def get_data():
    """Fetches historical data from the SQLite database."""
    try:
        conn = sqlite3.connect("irrigation_system.db")
        df = pd.read_sql_query("SELECT * FROM moisture_logs", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

# Layout: Creating two columns for Metrics
col1, col2 = st.columns(2)

df = get_data()

if not df.empty:
    latest_val = df['value'].iloc[-1]
    latest_status = df['status'].iloc[-1]
    
    with col1:
        st.metric(label="Current Soil Moisture", value=f"{latest_val}%")
    
    with col2:
        # Visual indicator for status
        if latest_status == "CRITICAL":
            st.error(f"System Status: {latest_status} (Needs Watering!)")
        else:
            st.success(f"System Status: {latest_status}")

    # Real-time Chart
    st.subheader("Moisture Levels Over Time")
    # Setting the timestamp as index for the chart
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_chart = df.set_index('timestamp')
    st.line_chart(df_chart['value'])

    # Historical Data Table
    with st.expander("View Raw Telemetry Logs"):
        st.write(df.tail(10).sort_values(by='timestamp', ascending=False))
else:
    st.info("Waiting for data... Please ensure the Manager and Node are running.")

# Auto-refresh logic (every 5 seconds)
time.sleep(5)
st.rerun()