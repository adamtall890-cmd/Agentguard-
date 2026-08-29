from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agent.runner import run_task
from engine.outcome import verify_outcome

app = FastAPI(
    title="AgentGuard",
    version="1.0"
)

# Sert les fichiers HTML/CSS/JS
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def dashboard():
    return FileResponse("frontend/index.html")


@app.get("/api")
def api():
    return {
        "message": "AgentGuard API",
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
        "task": task,
        "agent": agent_result,
        "verification": verification
    }

