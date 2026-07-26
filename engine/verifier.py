from engine.contradiction import detect_contradiction
from engine.scoring import score_sources


def verify_claim(claim: str, web_results: dict):

    score = score_sources(web_results.get("results", []))
    contradiction = detect_contradiction(claim, web_results)

    if contradiction is True:
        return {
            "verdict": "FALSE",
            "confidence": score,
            "reason": "Les sources fiables contredisent cette affirmation."
        }

    if contradiction is False:
        return {
            "verdict": "TRUE",
            "confidence": score,
            "reason": "Plusieurs sources fiables confirment cette affirmation."
        }

    return {
        "verdict": "yes or no",
        "confidence": score,
        "reason": "Les résultats Web ne permettent pas encore de conclure."
    }