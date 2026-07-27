from connectors.stripe import get_refund


def verify_outcome(refund_id: str):

    refund = get_refund(refund_id)

    expected = refund["expected_amount"]
    actual = refund["actual_amount"]

    if refund["status"] == "not_found":
        return {
            "refund_id": refund_id,
            "verdict": "FAKE_COMPLETION",
            "verified": False,
            "reason": "Refund does not exist in the source of truth.",
            "expected": expected,
            "actual": None
        }

    if actual == expected:
        return {
            "refund_id": refund_id,
            "verdict": "VERIFIED",
            "verified": True,
            "reason": "Business outcome confirmed.",
            "expected": expected,
            "actual": actual
        }

    if 0 < actual < expected:
        return {
            "refund_id": refund_id,
            "verdict": "PARTIAL",
            "verified": False,
            "reason": "Business outcome is only partially completed.",
            "expected": expected,
            "actual": actual
        }

    return {
        "refund_id": refund_id,
        "verdict": "FAKE_COMPLETION",
        "verified": False,
        "reason": "Agent reported success but business outcome is missing.",
        "expected": expected,
        "actual": actual
    }