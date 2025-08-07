# app/pages/home.py
import streamlit as st
from datetime import datetime
from app.utils.feedback_handler import save_feedback, load_feedback
from app.utils.error_handler import log_error

# Page Configuration
st.set_page_config(
    page_title="Suricata Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def display_header():
    """Display the page header"""
    st.title("Suricata Network Anomaly Detection")
    st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem !important;
        color: #1a5276;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3498db;
    }
    </style>
    <div class='main-title'>Suricata Network Anomaly Detection</div>
    """, unsafe_allow_html=True)

def display_metrics():
    """Display key metrics"""
    st.subheader("Performance Metrics")
    cols = st.columns(4)
    
    metrics = [
        ("Total Alerts", "1,245", "12% from yesterday"),
        ("Threats Detected", "87", "5.2% of total"),
        ("False Positives", "15", "3 below average"),
        ("Response Time", "42ms", "2ms improvement")
    ]
    
    for col, (label, value, delta) in zip(cols, metrics):
        with col:
            st.metric(label, value, delta)

def display_feedback_section():
    """Display and handle user feedback"""
    with st.expander("✉️ Provide Feedback", expanded=False):
        with st.form("feedback_form", clear_on_submit=True):
            st.write("Help us improve our service")
            
            # Feedback fields
            name = st.text_input("Your name (optional)", max_chars=50)
            feedback = st.text_area("Your feedback*", height=100)
            rating = st.select_slider("Rating", options=[1, 2, 3, 4, 5], value=3)
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                if not feedback.strip():
                    st.warning("Please enter your feedback")
                else:
                    metadata = {
                        "rating": rating,
                        "user_agent": st.experimental_get_query_params().get("user_agent", [""])[0],
                        "screen_width": st.experimental_get_query_params().get("width", [""])[0]
                    }
                    
                    if save_feedback(
                        user_input=feedback,
                        page="home",
                        metadata={
                            "name": name if name else "Anonymous",
                            "rating": rating,
                            "user_platform": "web"
                        }
                    ):
                        st.success("Thank you for your feedback!")
                    else:
                        st.error("Failed to submit feedback. Please try again.")

def display_feedback_history():
    """Display recent feedback (admin view)"""
    if st.checkbox("Show recent feedback (admin)"):
        feedback_data = load_feedback()
        if feedback_data:
            st.subheader("Recent Feedback")
            for idx, entry in enumerate(reversed(feedback_data[-5:]), 1):
                with st.expander(f"Feedback #{idx} - {entry.get('timestamp', '')}"):
                    st.write(f"**Page:** {entry.get('page', 'N/A')}")
                    st.write(f"**Rating:** {entry.get('metadata', {}).get('rating', 'N/A')}/5")
                    st.write(f"**Feedback:** {entry.get('feedback', '')}")
                    if entry.get('metadata', {}).get('name'):
                        st.write(f"**From:** {entry['metadata']['name']}")

def main():
    try:
        display_header()
        display_metrics()
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs(["Dashboard", "Analysis", "Reports"])
        
        with tab1:
            st.subheader("Real-time Monitoring")
            st.line_chart([10, 25, 30, 45, 60, 55, 80])
        
        with tab2:
            st.subheader("Threat Analysis")
            st.write("Detailed threat analysis will appear here")
        
        with tab3:
            st.subheader("Generated Reports")
            st.write("System reports will appear here")
        
        display_feedback_section()
        display_feedback_history()
        
    except Exception as e:
        log_error(e, "home_page")
        st.error("An error occurred while loading the page. Our team has been notified.")
        st.button("Reload Page")

if __name__ == "__main__":
    main()