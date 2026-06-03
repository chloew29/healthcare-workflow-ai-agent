import streamlit as st
import pandas as pd
from datetime import datetime

from utils.agent_tools import (
    classify_request,
    appointment_tool,
    prior_auth_tool,
    billing_claims_tool,
    estimate_agent_metrics
)

st.set_page_config(
    page_title="Healthcare Workflow AI Agent",
    page_icon="🏥",
    layout="wide"
)


st.title("🏥 Healthcare Workflow AI Agent")

st.markdown("""
An AI-agent-style healthcare operations platform that simulates patient access,
appointment routing, prior authorization checks, human escalation flags,
and agent performance analytics.

This project uses **synthetic healthcare operations data only** and does not contain PHI.
It is for educational and portfolio purposes only.
""")

st.caption(
    "Safety note: This project does not provide medical advice, diagnosis, treatment, "
    "insurance decisions, or real scheduling."
)

st.divider()


# -----------------------------
# Load synthetic data
# -----------------------------

appointments_df = pd.read_csv("data/appointments.csv")
providers_df = pd.read_csv("data/providers.csv")
payer_rules_df = pd.read_csv("data/payer_rules.csv")
claims_df = pd.read_csv("data/claims.csv")


# -----------------------------
# Core workflow function
# -----------------------------

def run_agent_workflow(message: str) -> dict:
    """
    Runs one full AI-agent-style workflow:
    1. Classify patient request
    2. Route to the correct operational tool
    3. Generate human escalation flag
    4. Estimate operational impact
    5. Return structured log row
    """

    classification = classify_request(message)
    intent = classification["intent"]

    if intent == "appointment":
        result = appointment_tool(classification, appointments_df, providers_df)

    elif intent == "prior_authorization":
        result = prior_auth_tool(classification, payer_rules_df)

    elif intent == "billing_claims":
        result = billing_claims_tool(classification, claims_df)

    else:
        result = {
            "status": "Needs human review",
            "reason": "Request type is not supported in the MVP.",
            "escalation_flag": True
        }

    metrics = estimate_agent_metrics(intent, result.get("escalation_flag", True))

    log_row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "message": message,
        "intent": intent,
        "department": classification.get("department"),
        "procedure_type": classification.get("procedure_type"),
        "payer": classification.get("payer"),
        "agent_status": result.get("status"),
        "escalation_flag": result.get("escalation_flag", True),
        "auto_resolved": metrics["auto_resolved"],
        "estimated_staff_minutes_saved": metrics["estimated_staff_minutes_saved"],
        "estimated_token_cost": metrics["estimated_token_cost"]
    }

    return {
        "classification": classification,
        "result": result,
        "metrics": metrics,
        "log_row": log_row
    }


def append_logs(new_logs: list):
    """
    Appends one or multiple workflow log rows to data/agent_logs.csv.
    """

    try:
        existing_logs_df = pd.read_csv("data/agent_logs.csv")
        updated_logs_df = pd.concat(
            [existing_logs_df, pd.DataFrame(new_logs)],
            ignore_index=True
        )

    except FileNotFoundError:
        updated_logs_df = pd.DataFrame(new_logs)

    updated_logs_df.to_csv("data/agent_logs.csv", index=False)


# -----------------------------
# Single request workflow
# -----------------------------

st.subheader("Patient Request Intake")

example_messages = [
    "I need to schedule a cardiology appointment next week.",
    "I have Kaiser HMO and need an MRI. Do I need approval?",
    "I want to book a primary care visit.",
    "I have Blue Shield PPO and need a specialist visit."
]

message = st.text_area(
    "Enter a synthetic patient request:",
    value=example_messages[0],
    height=120
)

if st.button("Run AI Agent Workflow"):
    workflow_output = run_agent_workflow(message)

    classification = workflow_output["classification"]
    result = workflow_output["result"]
    metrics = workflow_output["metrics"]
    log_row = workflow_output["log_row"]

    st.subheader("1. Request Classification")
    st.json(classification)

    st.subheader("2. Agent Tool Output")
    st.json(result)

    st.subheader("3. Operational Impact Estimate")
    st.json(metrics)

    append_logs([log_row])

    st.success("Workflow completed and logged.")


# -----------------------------
# Batch simulation workflow
# -----------------------------

st.divider()

st.subheader("Batch Agent Simulation")

st.markdown("""
Run a batch of synthetic healthcare requests to simulate how the AI agent performs across
appointment scheduling, prior authorization, and unsupported requests.
""")

sample_requests = [
    "I need to schedule a cardiology appointment next week.",
    "I have Kaiser HMO and need an MRI. Do I need approval?",
    "I have Blue Shield PPO and need a specialist visit.",
    "I want to book a primary care visit.",
    "I have Medicare Advantage and need an MRI.",
    "I need help with my bill.",
    "Can I schedule a dermatology appointment?",
    "I have Aetna PPO and need a specialist visit.",
    "I need to book an orthopedics appointment.",
    "I have Cigna PPO and need a primary care visit.",
    "Do I need insurance approval for an MRI with Blue Shield PPO?",
    "I want to reschedule my radiology appointment.",
    "I have Kaiser HMO and need a primary care visit.",
    "Can I cancel my appointment?",
    "I need prior authorization for a specialist visit with Aetna PPO.",
    "Can I book a dermatology visit this month?",
    "I need approval for an MRI with Medicare Advantage.",
    "I want to schedule an orthopedics visit.",
    "Does Blue Shield PPO cover a specialist visit?",
    "I have a question about my insurance bill."
    "I need to schedule a cardiology appointment next week.",
    "I have Kaiser HMO and need an MRI. Do I need approval?",
    "I have Blue Shield PPO and need a specialist visit.",
    "I want to book a primary care visit.",
    "I have Medicare Advantage and need an MRI.",
    "I need help with my bill.",
    "Can I schedule a dermatology appointment?",
    "I have Aetna PPO and need a specialist visit.",
    "I need to book an orthopedics appointment.",
    "I have Cigna PPO and need a primary care visit.",
    "Do I need insurance approval for an MRI with Blue Shield PPO?",
    "I want to reschedule my radiology appointment.",
    "I have Kaiser HMO and need a primary care visit.",
    "Can I cancel my appointment?",
    "I need prior authorization for a specialist visit with Aetna PPO.",
    "Can you check my claim status?",
    "Why was my claim denied?",
    "How much balance do I still owe?",
    "Can you explain my billing issue?",
    "My insurance payment is still pending."
]

batch_size = st.slider(
    "Number of synthetic requests to process",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

if st.button("Run Batch Simulation"):
    batch_logs = []

    for i in range(batch_size):
        synthetic_message = sample_requests[i % len(sample_requests)]
        workflow_output = run_agent_workflow(synthetic_message)
        batch_logs.append(workflow_output["log_row"])

    append_logs(batch_logs)

    st.success(f"Batch simulation completed. {batch_size} synthetic requests processed and logged.")


# -----------------------------
# Optional reset logs
# -----------------------------

with st.expander("Reset Agent Logs"):
    st.warning("This will clear data/agent_logs.csv and reset the dashboard.")

    if st.button("Clear Agent Logs"):
        empty_logs_df = pd.DataFrame(columns=[
            "timestamp",
            "message",
            "intent",
            "department",
            "procedure_type",
            "payer",
            "agent_status",
            "escalation_flag",
            "auto_resolved",
            "estimated_staff_minutes_saved",
            "estimated_token_cost"
        ])

        empty_logs_df.to_csv("data/agent_logs.csv", index=False)
        st.success("Agent logs cleared. Refresh the page to reset the dashboard.")


# -----------------------------
# Agent performance dashboard
# -----------------------------

st.divider()

st.subheader("Agent Performance Dashboard")

try:
    logs_df = pd.read_csv("data/agent_logs.csv")

    if logs_df.empty:
        st.info("No agent logs yet. Run the workflow or batch simulation above to generate analytics.")

    else:
        # Make boolean columns safe
        logs_df["auto_resolved"] = logs_df["auto_resolved"].astype(bool)
        logs_df["escalation_flag"] = logs_df["escalation_flag"].astype(bool)

        col1, col2, col3, col4, col5 = st.columns(5)

        total_requests = len(logs_df)
        auto_resolved_rate = logs_df["auto_resolved"].mean() * 100
        escalation_rate = logs_df["escalation_flag"].mean() * 100
        total_minutes_saved = logs_df["estimated_staff_minutes_saved"].sum()
        total_token_cost = logs_df["estimated_token_cost"].sum()

        col1.metric("Total Requests", total_requests)
        col2.metric("Auto-Resolved Rate", f"{auto_resolved_rate:.1f}%")
        col3.metric("Escalation Rate", f"{escalation_rate:.1f}%")
        col4.metric("Staff Minutes Saved", f"{total_minutes_saved:.0f}")
        col5.metric("Token Cost", f"${total_token_cost:.4f}")

        st.markdown("### Request Type Volume")
        request_volume = logs_df["intent"].value_counts()
        st.bar_chart(request_volume)

        st.markdown("### Auto-Resolved vs Escalated")
        resolution_df = logs_df["auto_resolved"].value_counts().rename(index={
            True: "Auto-Resolved",
            False: "Escalated / Human Review"
        })
        st.bar_chart(resolution_df)

        st.markdown("### Average Staff Minutes Saved by Intent")
        avg_saved_df = logs_df.groupby("intent")["estimated_staff_minutes_saved"].mean()
        st.bar_chart(avg_saved_df)

        st.markdown("### Escalation Rate by Intent")
        escalation_by_intent = logs_df.groupby("intent")["escalation_flag"].mean() * 100
        st.bar_chart(escalation_by_intent)

        st.markdown("### Token Cost by Intent")
        token_cost_by_intent = logs_df.groupby("intent")["estimated_token_cost"].sum()
        st.bar_chart(token_cost_by_intent)

        st.markdown("### Agent Logs")
        st.dataframe(logs_df, use_container_width=True)

except FileNotFoundError:
    st.info("No agent logs yet. Run the workflow or batch simulation above to generate analytics.")