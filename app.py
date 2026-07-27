from fastapi import FastAPI
from pydantic import BaseModel
from engine.outcome import verify_outcome
from connectors import crm
from connectors import web

from engine.fact_extractor import extract_facts
from engine.evidence import merge_evidence
from engine.verifier import verify_claim

app = FastAPI(title="AgentGuard")


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.8"
    }


class OutcomeRequest(BaseModel):
    refund_id: str


@app.post("/outcome")
def outcome(data: OutcomeRequest):
    return verify_outcome(data.refund_id)

    return {
        "claim": data.claim,
        "facts": facts,
        "evidence": evidence,
        "crm": crm_data,
        "web": web_data,
        **decision
    }