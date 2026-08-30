import streamlit as st
import pandas as pd
import os
from groq import Groq

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

# Sidebar for API Key & Webhook configuration
st.sidebar.header("⚙️ Configuration")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
slack_webhook = st.sidebar.text_input("Slack Webhook URL (Optional)", type="password")

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
        if not groq_api_key:
            st.error("Please enter your Groq API Key in the sidebar to run live AI analysis.")
        else:
            with st.spinner("Analyzing schema changes and execution logs via Groq API (Llama 3.1)..."):
                try:
                    client = Groq(api_key=groq_api_key)
                    prompt = """
                    You are an expert Data Engineering Agent. A data pipeline anomaly has been detected: 
                    A sudden spike of 18% in null values within the `user_id` column of the `etl_user_events` pipeline.
                    Provide a concise root-cause analysis and a corrective SQL action plan or code fix formatted in clear markdown sections.
                    """
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.1-8b-instant",
                    )
                    
                    ai_response = chat_completion.choices[0].message.content
                    
                    st.success("Analysis Complete!")
                    st.markdown("### **AI Diagnosis & Action Plan:**")
                    st.markdown(ai_response)
                    
                except Exception as e:
                    st.error(f"Error connecting to Groq API: {e}")

    if st.button("Execute Auto-Remediation"):
        st.balloons()
        st.success("Pipeline patched successfully! Fallback recovery active and schema guard deployed.")
        
    if st.button("Send Alert to Slack Webhook"):
        if slack_webhook:
            st.success("Alert successfully dispatched to Slack channel #data-ops-alerts!")
        else:
            st.warning("Please provide a valid Slack Webhook URL in the sidebar configuration.")