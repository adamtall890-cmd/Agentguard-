import requests
from urllib.parse import quote

def search(query: str):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={quote(query)}&limit=1&namespace=0&format=json"

        r = requests.get(url, timeout=10)
        data = r.json()

        results = []

        if len(data) >= 4 and len(data[1]) > 0:
            results.append({
                "title": data[1][0],
                "summary": data[2][0],
                "url": data[3][0]
            })

        return {
            "query": query,
            "results": results
        }

    except Exception as e:
        return {
            "query": query,
            "results": [],
            "error": str(e)
        }