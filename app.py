from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AgentGuard")


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.3"
    }


@app.post("/verify")
def verify(data: Claim):

    text = data.claim.lower()

    if "terre est plate" in text:
        return {
            "claim": data.claim,
            "verdict": "FALSE",
            "confidence": 0.99,
            "reason": "Les preuves scientifiques montrent que la Terre est sphérique."
        }

    if "2+2=4" in text:
        return {
            "claim": data.claim,
            "verdict": "TRUE",
            "confidence": 1.0,
            "reason": "Vérité mathématique."
        }

    return {
        "claim": data.claim,
        "verdict": "UNKNOWN",
        "confidence": 0.0,
        "reason": "Aucune règle disponible."
    }