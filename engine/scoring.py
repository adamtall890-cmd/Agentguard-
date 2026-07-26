def score_sources(results):

    score = 0

    for r in results:

        url = r.get("url", "").lower()

        if "wikipedia.org" in url:
            score += 20

        elif "larousse.fr" in url:
            score += 20

        elif ".gouv.fr" in url:
            score += 40

        elif ".gov" in url:
            score += 40

        elif ".edu" in url:
            score += 35

        elif "reuters.com" in url:
            score += 40

        elif "apnews.com" in url:
            score += 40

        else:
            score += 5

    return min(score, 100)
