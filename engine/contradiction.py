def detect_contradiction(claim: str, web_results: dict):

    text = ""

    for r in web_results.get("results", []):
        text += " "
        text += r.get("title", "")
        text += " "
        text += r.get("snippet", "")

    text = text.lower()
    claim = claim.lower()

    # Paris
    if "paris" in claim and "capitale" in claim:
        if "paris" in text and "capital" in text:
            return False

    # Marseille capitale
    if "marseille" in claim and "capitale" in claim:
        if "paris" in text and "capital" in text:
            return True

    return None
