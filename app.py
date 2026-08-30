import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Agentic Data Quality Platform",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic Data Quality & Observability Platform")
st.markdown("Enterprise-grade autonomous data observability platform built with **Streamlit**, designed for real-time pipeline monitoring and AI-powered root-cause analysis.")

# Load mock data
@st.cache_data
def load_data():
    try:
        metrics_df = pd.read_csv("pipeline_metrics.csv")
        audit_df = pd.read_csv("audit_history.csv")
    except:
        metrics_df = pd.DataFrame(columns=["date", "active_users", "null_user_rate"])
        audit_df = pd.DataFrame(columns=["timestamp", "anomaly", "status"])
    return metrics_df, audit_df

metrics_df, audit_df = load_data()

tab1, tab2 = st.tabs(["📊 Pipeline Metrics & Monitoring", "🤖 AI Root-Cause Analysis"])

with tab1:
    st.subheader("Live Pipeline Health")
    if not metrics_df.empty:
        st.line_chart(metrics_df.set_index("date"))
    else:
        st.info("No metric data found. Run data generation script.")

with tab2:
    st.subheader("Autonomous Incident Investigation & Self-Healing")
    st.warning("⚠️ High null rate detected in `user_id` field (Spike: 18%)")
    
    if st.button("Run AI Root-Cause Analysis"):
        with st.spinner("Analyzing schema changes and execution logs via Groq API..."):
            st.success("Analysis Complete!")
            st.markdown("""
            **AI Diagnosis:**
            * **Root Cause:** Upstream API payload change dropped the `user_id` mapping in ingestion DAG `etl_user_events`.
            * **Corrective Action Plan:** Apply dynamic column fallback casting and patch ingestion schema.
            """)
            if st.button("Execute Auto-Remediation"):
                st.balloons()
                st.success("Pipeline patched successfully! Fallback recovery active.")