def merge_evidence(web_results: dict):

    evidence = {
        "total_sources": 0,
        "titles": [],
        "urls": [],
        "snippets": []
    }

    for r in web_results.get("results", []):

        evidence["total_sources"] += 1

        evidence["titles"].append(
            r.get("title", "")
        )

        evidence["urls"].append(
            r.get("url", "")
        )

        evidence["snippets"].append(
            r.get("snippet", "")
        )

    return evidence
