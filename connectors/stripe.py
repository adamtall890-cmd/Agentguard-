def get_refund(refund_id: str):
    """
    Simulation Stripe.
    Permet de démontrer plusieurs scénarios d'Outcome Verification.
    """

    database = {
        "refund_ok": {
            "refund_id": "refund_ok",
            "payment_id": "pay_123456",
            "expected_amount": 100,
            "actual_amount": 100,
            "currency": "USD",
            "status": "succeeded"
        },

        "refund_partial": {
            "refund_id": "refund_partial",
            "payment_id": "pay_222222",
            "expected_amount": 100,
            "actual_amount": 80,
            "currency": "USD",
            "status": "partial"
        },

        "refund_missing": {
            "refund_id": "refund_missing",
            "payment_id": "pay_333333",
            "expected_amount": 100,
            "actual_amount": 0,
            "currency": "USD",
            "status": "missing"
        }
    }

    return database.get(
        refund_id,
        {
            "refund_id": refund_id,
            "payment_id": None,
            "expected_amount": 100,
            "actual_amount": 0,
            "currency": "USD",
            "status": "not_found"
        }
    )