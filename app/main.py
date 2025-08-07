# app/main.py
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json
import time
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
REFRESH_INTERVAL = 60  # seconds

# Session state initialization
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None
if 'data' not in st.session_state:
    st.session_state.data = None
if 'error' not in st.session_state:
    st.session_state.error = None

@st.cache_data(ttl=REFRESH_INTERVAL, show_spinner="Fetching anomaly data...")
def fetch_anomalies_json() -> Optional[pd.DataFrame]:
    """
    Fetch anomalies data from backend API with authentication
    
    Returns:
        Optional[pd.DataFrame]: DataFrame containing anomalies or None if error occurs
    """
    try:
        response = requests.get(
            f"{BACKEND_URL}/anomalies/json",
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            timeout=10
        )
        response.raise_for_status()
        return pd.DataFrame(response.json())
    
    except requests.exceptions.RequestException as e:
        st.session_state.error = f"API request failed: {str(e)}"
        return None
    except (json.JSONDecodeError, ValueError) as e:
        st.session_state.error = f"Data parsing error: {str(e)}"
        return None

def display_status_bar():
    """Display refresh status and last update time"""
    if st.session_state.last_refresh:
        last_refresh_str = datetime.fromtimestamp(
            st.session_state.last_refresh
        ).strftime("%Y-%m-%d %H:%M:%S")
        
        status_cols = st.columns(3)
        with status_cols[0]:
            st.metric("Last Refresh", last_refresh_str)
        with status_cols[1]:
            st.metric("Next Refresh In", 
                     f"{REFRESH_INTERVAL - (time.time() - st.session_state.last_refresh):.0f}s")
        with status_cols[2]:
            if st.button("🔄 Refresh Now"):
                st.cache_data.clear()
                st.session_state.last_refresh = time.time()
                st.rerun()

def download_buttons(df: pd.DataFrame):
    """Generate download buttons for the data"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    st.download_button(
        label="📊 Download CSV",
        data=df.to_csv(index=False),
        file_name=f"anomalies_{timestamp}.csv",
        mime="text/csv",
        help="Download data in CSV format"
    )

    st.download_button(
        label="📝 Download JSON",
        data=df.to_json(orient="records", indent=2),
        file_name=f"anomalies_{timestamp}.json",
        mime="application/json",
        help="Download data in JSON format"
    )

def display_data_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Display interactive data filters"""
    st.sidebar.header("Data Filters")
    
    # Severity filter
    if 'severity' in df.columns:
        severity_levels = df['severity'].unique()
        selected_severity = st.sidebar.multiselect(
            "Severity Level",
            options=sorted(severity_levels),
            default=sorted(severity_levels)
        )
        df = df[df['severity'].isin(selected_severity)]
    
    # Date filter (if timestamp exists)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        min_date = df['timestamp'].min().to_pydatetime()
        max_date = df['timestamp'].max().to_pydatetime()
        
        date_range = st.sidebar.slider(
            "Date Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )
        df = df[(df['timestamp'] >= date_range[0]) & 
                (df['timestamp'] <= date_range[1])]
    
    return df

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="Anomaly Monitoring",
        layout="wide",
        page_icon="🚨"
    )
    
    st.title("🚨 Anomaly Detection Dashboard")
    st.markdown("### Real-time Network Threat Monitoring")
    
    # Fetch data
    df_anomalies = fetch_anomalies_json()
    st.session_state.last_refresh = time.time()
    
    # Display status and error messages
    display_status_bar()
    
    if st.session_state.error:
        st.error(st.session_state.error)
    
    if df_anomalies is None:
        st.warning("Failed to load anomaly data. Please try again later.")
        return
    
    if df_anomalies.empty:
        st.success("✅ No anomalies detected in the current time period.")
        return
    
    # Apply filters
    filtered_df = display_data_filters(df_anomalies)
    
    # Display data
    st.subheader(f"Detected Anomalies ({len(filtered_df)} records)")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600,
        hide_index=True
    )
    
    # Download options
    st.subheader("Data Export")
    download_buttons(filtered_df)
    
    # Data statistics
    with st.expander("📈 Data Statistics"):
        st.write(filtered_df.describe(include='all', datetime_is_numeric=True))

if __name__ == "__main__":
    main()