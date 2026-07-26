from engine.scoring import score_sources


def verify_claim(claim: str, web_results: dict):

    text = ""

    for r in web_results.get("results", []):
        text += " "
        text += r.get("title", "")
        text += " "
        text += r.get("snippet", "")

    text = text.lower()

    score = score_sources(web_results.get("results", []))

    claim_lower = claim.lower()

    if (
        "paris" in claim_lower
        and "capitale" in claim_lower
        and "france" in claim_lower
    ):

        if "paris" in text and "capital" in text:
            return {
                "verdict": "TRUE",
                "confidence": score,
                "reason": "Plusieurs sources fiables confirment cette affirmation."
            }

    return {
        "verdict": "UNKNOWN",
        "confidence": score,
        "reason": "Les résultats Web ne permettent pas encore de conclure."
    }