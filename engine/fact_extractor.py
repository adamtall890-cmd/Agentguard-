import re


def extract_facts(claim: str):

    claim = claim.strip()

    facts = {
        "subject": None,
        "relation": None,
        "object": None,
        "date": None,
        "original": claim
    }

    # Détection d'une année
    year = re.search(r"\b(19|20)\d{2}\b", claim)

    if year:
        facts["date"] = year.group()

    words = claim.split()

    if len(words) >= 3:

        facts["subject"] = words[0]

        facts["relation"] = " ".join(words[1:3])

        facts["object"] = " ".join(words[3:])

    return facts
