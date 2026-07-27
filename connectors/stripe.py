def get_refund(refund_id: str):
    """
    Simulation d'un remboursement Stripe.
    Plus tard on remplacera ceci par l'API Stripe.
    """

    return {
        "refund_id": refund_id,
        "payment_id": "pay_123456",
        "expected_amount": 100,
        "actual_amount": 100,
        "currency": "USD",
        "status": "succeeded"
    }
