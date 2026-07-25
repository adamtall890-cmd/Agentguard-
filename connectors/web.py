import requests

def search(query: str):
    """
    Connecteur Web simple
    """
    return {
        "query": query,
        "results": [
            {
                "title": "Wikipedia",
                "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
            }
        ]
    }
