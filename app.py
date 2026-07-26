from fastapi import FastAPI
from pydantic import BaseModel

from connectors import crm
from connectors import web

from engine.fact_extractor import extract_facts
from engine.verifier import verify_claim

app = FastAPI(title="AgentGuard")


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.7"
    }


@app.post("/verify")
def verify(data: Claim):

    facts = extract_facts(data.claim)

    crm_data = crm.read()

    web_data = web.search(data.claim)

    decision = verify_claim(data.claim, web_data)

    return {
        "claim": data.claim,
        "facts": facts,
        "crm": crm_data,
        "web": web_data,
        **decision
    }