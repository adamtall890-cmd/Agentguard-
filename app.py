from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi import FastAPI
from pydantic import BaseModel

from agent.runner import run_task
from engine.outcome import verify_outcome

app = FastAPI(
    title="AgentGuard",
    version="1.0"
)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/demo")
def demo():
    return FileResponse("frontend/index.html")

@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "1.0"
    }


class OutcomeRequest(BaseModel):
    refund_id: str


@app.post("/outcome")
def outcome(data: OutcomeRequest):

    # Objectif donné à l'agent
    task = {
        "action": "CREATE_LEAD",
        "lead_id": data.refund_id
    }

    # L'agent exécute la tâche
    agent_result = run_task(task)

    # AgentGuard vérifie indépendamment le résultat
    verification = verify_outcome(data.refund_id)

    return {
        "task": task,
        "agent": agent_result,
        "verification": verification
    }