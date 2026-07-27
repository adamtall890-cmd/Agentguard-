@app.post("/outcome")
def outcome(data: OutcomeRequest):

    # Objectif donné à l'agent
    task = {
        "action": "CREATE_LEAD",
        "lead_id": data.refund_id
    }

    # L'agent exécute la tâche
    agent_result = run_task(task)

    # AgentGuard vérifie indépendamment
    verification = verify_outcome(data.refund_id)

    return {
        "agent": agent_result,
        "verification": verification
    }