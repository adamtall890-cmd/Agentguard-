def execute_workflow(workflow: str):
    """
    Simule un agent IA.
    L'agent annonce toujours SUCCESS.
    """

    return {
        "workflow": workflow,
        "agent_status": "SUCCESS",
        "message": "Task completed successfully."
    }
