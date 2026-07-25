from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="AgentGuard")


class VerificationRequest(BaseModel):
    expected_state: dict
    actual_state: dict


@app.get("/")
def home():
    return {
        "message": "AgentGuard is running",
        "version": "0.6"
    }


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

    mismatches = compare_states(
        data.expected_state,
        data.actual_state
    )

    if len(mismatches) == 0:

        return {
            "verdict": "PASSED",
            "confidence": 1.0,
            "message": "Expected state matches actual state.",
            "mismatches": [],
            "generated_at": datetime.utcnow().isoformat()
        }

    return {
        "verdict": "FAILED",
        "confidence": 1.0,
        "message": "Differences detected.",
        "mismatches": mismatches,
        "generated_at": datetime.utcnow().isoformat()
    }