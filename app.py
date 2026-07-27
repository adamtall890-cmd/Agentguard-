from fastapi import FastAPI
from pydantic import BaseModel

from agent.runner import run_task
from engine.outcome import verify_outcome

app = FastAPI(title="AgentGuard")

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

    task = {
        "action": "CREATE_LEAD",
        "lead_id": data.refund_id
    }

    agent_result = run_task(task)

    verification = verify_outcome(data.refund_id)

    return {
        "agent": agent_result,
        "verification": verification
    }