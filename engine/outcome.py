from connectors.stripe import get_refund


def verify_outcome(refund_id: str):

    refund = get_refund(refund_id)

    expected = refund["expected_amount"]
    actual = refund["actual_amount"]

    success = expected == actual

    return {
        "refund_id": refund_id,
        "expected": expected,
        "actual": actual,
        "verified": success,
        "reason": (
            "Refund matches expected amount."
            if success
            else "Refund amount mismatch."
        )
    }
