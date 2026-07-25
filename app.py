from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="AgentGuard")


class VerificationRequest(BaseModel):
    expected_state: dict


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.7"
    }


# ==========================================
# Fake CRM (sera remplacé plus tard)
# ==========================================

def read_crm():

    return {
        "customer": "John",
        "status": "Pending",
        "invoice": "INV-001"
    }


# ==========================================

def compare_states(expected: dict, actual: dict):

    mismatches = []

    for key, expected_value in expected.items():

        actual_value = actual.get(key)

        if actual_value != expected_value:

            mismatches.append({
                "field": key,
                "expected": expected_value,
                "actual": actual_value
            })

    return mismatches


@app.post("/verify")
def verify(data: VerificationRequest):

    actual_state = read_crm()

    mismatches = compare_states(
        data.expected_state,
        actual_state
    )

    if len(mismatches) == 0:

        return {
            "verdict": "PASSED",
            "actual_state": actual_state,
            "mismatches": [],
            "generated_at": datetime.utcnow().isoformat()
        }

    return {
        "verdict": "FAILED",
        "actual_state": actual_state,
        "mismatches": mismatches,
        "generated_at": datetime.utcnow().isoformat()
    }