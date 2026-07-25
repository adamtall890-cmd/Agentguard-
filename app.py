from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AgentGuard")


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.2"
    }


@app.post("/verify")
def verify(data: Claim):
    return {
        "claim": data.claim,
        "status": "received",
        "message": "Verification started."
    }