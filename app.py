import streamlit as st
import pandas as pd
import os
from groq import Groq

from utils.slack_alert import send_slack_alert

st.set_page_config(
    page_title="Agentic Data Quality Platform",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic Data Quality & Observability Platform")
st.markdown(
    "A prototype dashboard for pipeline monitoring and LLM-assisted root-cause analysis, "
    "built with **Streamlit**. All data shown here is synthetic."
)

# Load mock data
@st.cache_data
def load_data():
    try:
        metrics_df = pd.read_csv("pipeline_metrics.csv")
        audit_df = pd.read_csv("audit_history.csv")
    except FileNotFoundError:
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
    st.subheader("Pipeline Health (synthetic data)")
    if not metrics_df.empty:
        st.line_chart(metrics_df.set_index("date"))
    else:
        st.info("No metric data found. Run data generation script.")

with tab2:
    st.subheader("Incident Investigation (demo scenario)")
    st.warning("⚠️ Demo scenario: high null rate detected in `user_id` field (spike: 18%)")
    st.caption(
        "The anomaly above is a fixed example. The AI analysis and the Slack alert are real calls; "
        "auto-remediation is simulated."
    )

    if st.button("Run AI Root-Cause Analysis"):
        if not groq_api_key:
            st.error("Please enter your Groq API Key in the sidebar to run live AI analysis.")
        else:
            with st.spinner("Generating root-cause analysis for the sample anomaly via Groq (gpt-oss-120b)..."):
                try:
                    client = Groq(api_key=groq_api_key)
                    prompt = """
                    You are an expert Data Engineering Agent. A data pipeline anomaly has been detected: 
                    A sudden spike of 18% in null values within the `user_id` column of the `etl_user_events` pipeline.
                    Provide a concise root-cause analysis and a corrective SQL action plan or code fix formatted in clear markdown sections.
                    """

                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="openai/gpt-oss-120b",
                    )

                    ai_response = chat_completion.choices[0].message.content

                    st.success("Analysis Complete!")
                    st.markdown("### **AI Diagnosis & Action Plan:**")
                    st.markdown(ai_response)

                except Exception as e:
                    st.error(f"Error connecting to Groq API: {e}")

    if st.button("Execute Auto-Remediation (simulated)"):
        st.info("Simulation only: no changes were made to any pipeline.")

    if st.button("Send Alert to Slack Webhook"):
        if not slack_webhook:
            st.warning("Please provide a valid Slack Webhook URL in the sidebar configuration.")
        else:
            total_rows = len(metrics_df)
            missing_vals = int(metrics_df.isnull().sum().sum())
            cells = total_rows * metrics_df.shape[1]
            quality_score = 100 * (1 - missing_vals / cells) if cells else 0.0
            if send_slack_alert(slack_webhook, quality_score, total_rows, missing_vals):
                st.success("Alert sent to Slack.")
            else:
                st.error("Slack did not accept the alert. Check the webhook URL.")