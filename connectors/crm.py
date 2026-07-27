def get_lead(lead_id: str):
    """
    Simulation d'un CRM.
    """

    database = {
        "lead_ok": {
            "lead_id": "lead_ok",
            "email": "alice@test.com",
            "company": "OpenAI",
            "status": "created"
        },

        "lead_partial": {
            "lead_id": "lead_partial",
            "email": "bob@test.com",
            "company": "",
            "status": "created"
        },

        "lead_missing": None
    }

    return database.get(lead_id)