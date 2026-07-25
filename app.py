from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AgentGuard")


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.4"
    }


# -----------------------------
# AgentGuard Verification Pipeline
# -----------------------------

def understand_claim(text: str):
    return text


def extract_facts(text: str):
    return [text]


def search_evidence(facts):
    return []


def compare_evidence(evidence):
    return {}


def calculate_confidence(result):
    return 0.0


def verify_claim(text: str):

    claim = understand_claim(text)

    facts = extract_facts(claim)

    evidence = search_evidence(facts)

    comparison = compare_evidence(evidence)

    confidence = calculate_confidence(comparison)

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
        "confidence": confidence,
        "reason": "Aucune preuve disponible."
    }


@app.post("/verify")
def verify(data: Claim):

    result = verify_claim(data.claim)

    return {
        "claim": data.claim,
        **result
    }