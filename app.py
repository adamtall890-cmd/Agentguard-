from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="AgentGuard")


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.5"
    }


# ======================================
# AgentGuard Pipeline
# ======================================

def understand_claim(text: str):
    return {
        "original": text,
        "normalized": text.strip()
    }


def extract_facts(claim):
    return [
        claim["normalized"]
    ]


def search_evidence(facts):
    return []


def compare_evidence(evidence):
    return {
        "supported": [],
        "contradicted": []
    }


def calculate_confidence(comparison):
    return 0.0


def build_report(claim, verdict, confidence, reason, facts):

    return {
        "claim": claim,
        "verdict": verdict,
        "confidence": confidence,
        "facts_checked": facts,
        "reason": reason,
        "sources": [],
        "generated_at": datetime.utcnow().isoformat()
    }


def verify_claim(text: str):

    claim = understand_claim(text)

    facts = extract_facts(claim)

    evidence = search_evidence(facts)

    comparison = compare_evidence(evidence)

    confidence = calculate_confidence(comparison)

    normalized = claim["normalized"].lower()

    if "terre est plate" in normalized:

        return build_report(
            claim=text,
            verdict="FALSE",
            confidence=0.99,
            reason="Les preuves scientifiques montrent que la Terre est sphérique.",
            facts=facts
        )

    if "2+2=4" in normalized:

        return build_report(
            claim=text,
            verdict="TRUE",
            confidence=1.0,
            reason="Vérité mathématique.",
            facts=facts
        )

    return build_report(
        claim=text,
        verdict="UNKNOWN",
        confidence=confidence,
        reason="Aucune preuve disponible.",
        facts=facts
    )


@app.post("/verify")
def verify(data: Claim):

    return verify_claim(data.claim)