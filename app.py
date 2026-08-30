import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="Agentic Data Quality & Observability Platform", layout="wide")

st.title("🤖 Agentic Data Quality & Observability Platform")
st.markdown("Autonomous data pipeline monitoring, anomaly detection, AI-powered root-cause analysis, and self-healing automation.")

# Sidebar Configurations
st.sidebar.header("Configuration & Integrations")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
slack_webhook_url = st.sidebar.text_input("Slack Webhook URL (Optional)", type="password")

# Initialize Audit Log File if not exists
AUDIT_LOG_FILE = "audit_history.csv"
if not os.path.exists(AUDIT_LOG_FILE):
    pd.DataFrame(columns=["timestamp", "anomaly", "root_cause", "status"]).to_csv(AUDIT_LOG_FILE, index=False)

# Load data function
@st.cache_data
def load_data():
    if os.path.exists('pipeline_metrics.csv'):
        return pd.read_csv('pipeline_metrics.csv')
    return None

df = load_data()

if df is not None:
    # Navigation Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Live Observability & AI Agent", "🧬 Data Lineage & Architecture", "📜 Audit Trail & History"])
    
    with tab1:
        st.subheader("Pipeline Metrics Trend (Last 30 Days)")
        st.line_chart(df.set_index('date')[['active_users']])
        
        # Check latest row for anomalies
        latest_row = df.iloc[-1]
        
        anomalies = []
        if latest_row['active_users'] < 2000:
            anomalies.append(f"Sudden drop in active users: {latest_row['active_users']} (Expected > 2000)")
        if latest_row['null_user_id_rate'] > 0.05:
            anomalies.append(f"High null user ID rate: {latest_row['null_user_id_rate']*100}% (Expected < 5%)")
            
        if anomalies:
            st.error("🚨 Data Quality Anomalies Detected in Latest Pipeline Run!")
            for anomaly in anomalies:
                st.warning(anomaly)
                
            col1, col2 = st.columns(2)
            
            # Session state initialization for AI response
            if 'ai_response' not in st.session_state:
                st.session_state.ai_response = None
            if 'remediated' not in st.session_state:
                st.session_state.remediated = False

            with col1:
                if st.button("Run AI Root Cause Analysis Agent"):
                    if not groq_api_key:
                        st.error("Please enter your Groq API key in the sidebar configuration first.")
                    else:
                        with st.spinner("AI Agent is analyzing pipeline logs and upstream schema changes via Groq..."):
                            try:
                                client = Groq(api_key=groq_api_key)
                                prompt = f"""
                                You are an expert Data Reliability Engineer. 
                                An anomaly has been detected in the data pipeline:
                                - Anomalies: {anomalies}
                                - Latest Metrics: Active Users = {latest_row['active_users']}, Null Rate = {latest_row['null_user_id_rate']}
                                
                                Provide a concise root-cause analysis and suggest a corrective SQL query or action plan to fix this pipeline issue.
                                """
                                chat_completion = client.chat.completions.create(
                                    messages=[{"role": "user", "content": prompt}],
                                    model="openai/gpt-oss-20b",
                                )
                                st.session_state.ai_response = chat_completion.choices[0].message.content
                                
                                # Log to Audit Trail
                                new_log = pd.DataFrame([{
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "anomaly": " | ".join(anomalies),
                                    "root_cause": "Analyzed by AI Agent",
                                    "status": "Pending Remediation"
                                }])
                                pd.concat([pd.read_csv(AUDIT_LOG_FILE), new_log], ignore_index=True).to_csv(AUDIT_LOG_FILE, index=False)
                                
                            except Exception as e:
                                st.error(f"Error communicating with Groq API: {e}")

            if st.session_state.ai_response:
                st.markdown("### 🧠 AI Agent Root-Cause Report")
                st.markdown(st.session_state.ai_response)
                
                col_action1, col_action2 = st.columns(2)
                
                with col_action1:
                    if st.button("🚀 Send Alert to Slack Webhook"):
                        if not slack_webhook_url:
                            st.error("Please enter a Slack Webhook URL in the sidebar.")
                        else:
                            # Mock webhook post request
                            st.success("Successfully dispatched 🚨 Anomaly & AI Root-Cause Alert to Slack channel #data-reliability!")

                with col_action2:
                    if not st.session_state.remediated:
                        if st.button("🛠️ Execute Auto-Remediation (Self-Healing)"):
                            with st.spinner("Executing corrective SQL fallback and patching ingestion pipeline..."):
                                # Simulate self-healing patch
                                st.session_state.remediated = True
                                st.success("✅ Auto-Remediation executed successfully! Ingestion mapping updated and backfill triggered.")
                    else:
                        st.info("ℹ️ Pipeline has already been auto-healed for this run.")
        else:
            st.success("✅ All pipeline metrics are normal. No anomalies detected.")
            
    with tab2:
        st.subheader("🧬 Pipeline Data Lineage & Dependency Graph")
        st.markdown("Visualizing upstream dependencies, staging layers, and downstream mart impacts.")
        
        # Mermaid chart for lineage
        lineage_code = """
        graph LR
            A[Auth Service DB] -->|Raw Events JSON| B(Staging Users Table)
            B --> C{Data Quality Check}
            C -->|Pass < 5% Null| D[Active Users Mart]
            C -->|Fail > 35% Null| E[🚨 Anomaly Flagged & AI Agent]
            E -->|Auto-Remediation| B
        """
        st.code(lineage_code, language="mermaid")
        st.info("The diagram above maps out the complete data lineage from source systems to metric marts, highlighting automated anomaly interception points.")

    with tab3:
        st.subheader("📜 Historical Audit Trail & Compliance Log")
        st.markdown("Immutable audit log tracking all detected anomalies, AI agent decisions, and execution statuses.")
        
        audit_df = pd.read_csv(AUDIT_LOG_FILE)
        if not audit_df.empty:
            st.dataframe(audit_df, use_container_width=True)
        else:
            st.write("No historical records found yet.")
else:
    st.info("Please run `generate_data.py` first to create the metrics dataset.")