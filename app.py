from fastapi import FastAPI
from pydantic import BaseModel

from connectors import crm
from connectors import web
from engine.verifier import verify_claim

app = FastAPI(title="AgentGuard")


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.5"
    }


@app.post("/verify")
def verify(data: Claim):
    crm_data = crm.read()
    web_data = web.search(data.claim)
return {
    "claim": claim.text,
    "crm": crm_result,
    "web": web_result,
    **decision
}
