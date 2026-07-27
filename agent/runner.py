def run_task(task: dict):
    """
    Simule l'exécution d'une tâche par un agent IA.

    Plus tard, cette fonction appellera un vrai agent
    (OpenAI, Claude, LangGraph, etc.).

    Pour le prototype V1, elle retourne simplement
    ce que l'agent prétend avoir fait.
    """

    return {
        "status": "SUCCESS",
        "task": task,
        "message": "Agent reports task completed."
    }
