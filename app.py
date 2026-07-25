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

def verify_claim(text: str):

    text = text.lower()

    if "terre est plate" in text:
        return {
            "verdict": "FALSE",
            "confidence": 0.99,
            "reason": "Les preuves scientifiques montrent que la Terre est sphérique."
        }

    if "2+2=4" in text:
        return {
            "verdict": "TRUE",
            "confidence": 1.0,
            "reason": "Vérité mathématique."
        }

    return {
        "verdict": "UNKNOWN",
        "confidence": 0.0,
        "reason": "Aucune preuve disponible."
    }
@app.post("/verify")
def verify(data: Claim):

    result = verify_claim(data.claim)

    return {
        "claim": data.claim,
        **result
    }