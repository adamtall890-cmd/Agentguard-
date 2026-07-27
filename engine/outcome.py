from connectors.crm import get_lead


def verify_outcome(lead_id: str):
    """
    AgentGuard ne fait pas confiance à l'agent.
    Il vérifie directement l'état réel du CRM.
    """

    lead = get_lead(lead_id)

    if lead is None:
        return {
            "verified": False,
            "status": "missing",
            "reason": "Lead not found in CRM."
        }

    required_fields = [
        "name",
        "email",
        "status"
    ]

    missing = []

    for field in required_fields:
        value = lead.get(field)

        if value is None or value == "":
            missing.append(field)

    if missing:
        return {
            "verified": False,
            "status": "partial",
            "reason": "Missing required fields.",
            "missing_fields": missing,
            "lead": lead
        }

    if lead["status"] != "created":
        return {
            "verified": False,
            "status": "invalid",
            "reason": "Lead has incorrect status.",
            "lead": lead
        }

    return {
        "verified": True,
        "status": "verified",
        "reason": "Business outcome verified.",
        "lead": lead
    }