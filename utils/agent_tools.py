import pandas as pd


def classify_request(message: str) -> dict:
    """
    Rule-based request classifier for MVP.
    Later, this can be upgraded to an LLM-based classifier.
    """
    msg = message.lower()

    # Detect intent
    if any(word in msg for word in ["bill", "billing", "claim", "payment", "balance", "denied", "denial"]):
        intent = "billing_claims"
    elif any(word in msg for word in ["appointment", "schedule", "book", "reschedule", "cancel", "visit"]):
        intent = "appointment"
    elif any(word in msg for word in ["prior authorization", "authorization", "approval", "insurance", "covered", "authorize", "mri"]):
        intent = "prior_authorization"
    else:
        intent = "general_question"

    # Detect department
    departments = ["cardiology", "primary care", "radiology", "dermatology", "orthopedics"]
    department = None
    for d in departments:
        if d in msg:
            department = d.title()

    # Detect procedure type
    procedures = ["mri", "specialist visit", "primary care visit"]
    procedure_type = None
    for p in procedures:
        if p in msg:
            procedure_type = "MRI" if p == "mri" else p.title()

    # Detect payer
    payers = ["kaiser hmo", "blue shield ppo", "medicare advantage", "aetna ppo", "cigna ppo"]
    payer = None
    for payer_name in payers:
        if payer_name in msg:
            payer = payer_name.title()

    return {
        "intent": intent,
        "department": department,
        "procedure_type": procedure_type,
        "payer": payer,
        "original_message": message
    }


def appointment_tool(classification: dict, appointments_df: pd.DataFrame, providers_df: pd.DataFrame) -> dict:
    """
    Simulates appointment routing using synthetic appointment and provider data.
    """
    department = classification.get("department")

    if not department:
        return {
            "status": "Needs human review",
            "reason": "Department was not identified from the patient request.",
            "escalation_flag": True
        }

    matches = appointments_df[
        (appointments_df["department"].str.lower() == department.lower()) &
        (appointments_df["status"] == "Available")
    ]

    if matches.empty:
        return {
            "status": "Needs human review",
            "reason": f"No available appointment found for {department}.",
            "escalation_flag": True
        }

    appt = matches.iloc[0]
    provider_match = providers_df[providers_df["provider_id"] == appt["provider_id"]]

    if provider_match.empty:
        return {
            "status": "Needs human review",
            "reason": "Provider information was not found.",
            "escalation_flag": True
        }

    provider = provider_match.iloc[0]

    return {
        "status": "Appointment option found",
        "department": department,
        "provider": provider["provider_name"],
        "available_date": appt["available_date"],
        "estimated_wait_days": int(provider["next_available_days"]),
        "accepting_new_patients": provider["accepting_new_patients"],
        "escalation_flag": False
    }


def prior_auth_tool(classification: dict, payer_rules_df: pd.DataFrame) -> dict:
    """
    Simulates prior authorization checking using synthetic payer rules.
    """
    payer = classification.get("payer")
    procedure = classification.get("procedure_type")

    if not payer or not procedure:
        return {
            "status": "Needs human review",
            "reason": "Missing payer or procedure type.",
            "escalation_flag": True
        }

    matches = payer_rules_df[
        (payer_rules_df["payer"].str.lower() == payer.lower()) &
        (payer_rules_df["procedure_type"].str.lower() == procedure.lower())
    ]

    if matches.empty:
        return {
            "status": "Needs human review",
            "reason": "No matching prior authorization rule found.",
            "escalation_flag": True
        }

    rule = matches.iloc[0]
    high_risk = rule["denial_risk"] == "High"

    return {
        "status": "Prior authorization checked",
        "payer": rule["payer"],
        "procedure_type": rule["procedure_type"],
        "prior_auth_required": rule["prior_auth_required"],
        "required_documents": rule["required_documents"],
        "denial_risk": rule["denial_risk"],
        "escalation_flag": high_risk
    }


def estimate_agent_metrics(intent: str, escalation_flag: bool) -> dict:
    """
    Simulates operational impact from the AI agent workflow.
    """
    if escalation_flag:
        minutes_saved = 3
    else:
        minutes_saved = 12

    estimated_token_cost = 0.002

    return {
        "auto_resolved": not escalation_flag,
        "estimated_staff_minutes_saved": minutes_saved,
        "estimated_token_cost": estimated_token_cost
    }

def billing_claims_tool(classification: dict, claims_df: pd.DataFrame) -> dict:
    """
    Simulates a billing / claims workflow using synthetic revenue cycle data.
    This tool does not make real insurance or payment decisions.
    """

    # For MVP, use the first claim as a simulated match.
    # Later, this can be upgraded to search by patient account ID or claim ID.
    if claims_df.empty:
        return {
            "status": "Needs human review",
            "reason": "No claims data available.",
            "escalation_flag": True
        }

    claim = claims_df.sample(1).iloc[0]

    claim_status = claim["claim_status"]
    denial_reason = claim["denial_reason"]

    escalation_flag = False

    if claim_status in ["Denied", "Pending"]:
        escalation_flag = True

    return {
        "status": "Billing / claims workflow checked",
        "claim_id": claim["claim_id"],
        "payer": claim["payer"],
        "claim_amount": float(claim["claim_amount"]),
        "approved_amount": float(claim["approved_amount"]),
        "claim_status": claim_status,
        "denial_reason": denial_reason,
        "days_to_payment": int(claim["days_to_payment"]),
        "balance_due": float(claim["balance_due"]),
        "escalation_flag": escalation_flag
    }