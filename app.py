from fastapi import FastAPI
from pydantic import BaseModel

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
    return verify_outcome(data.refund_id)