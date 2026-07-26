def verify_claim(claim: str, web_results: dict):

    text = ""

    for r in web_results.get("results", []):
        text += " "
        text += r.get("title", "")
        text += " "
        text += r.get("snippet", "")

    text = text.lower()

    claim_lower = claim.lower()

    if "paris" in claim_lower and "capitale" in claim_lower and "france" in claim_lower:

        if "paris" in text and "capital" in text:
            return {
                "verdict": "TRUE",
                "confidence": 95,
                "reason": "Plusieurs résultats Web confirment cette affirmation."
            }

    return {
        "verdict": "UNKNOWN",
        "confidence": 25,
        "reason": "Les résultats ne permettent pas encore de conclure."
    }
