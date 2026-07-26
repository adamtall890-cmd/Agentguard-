import requests

def search(query: str):
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")

        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            data = r.json()

            return {
                "query": query,
                "results": [
                    {
                        "title": data.get("title"),
                        "summary": data.get("extract"),
                        "url": data.get("content_urls", {})
                                  .get("desktop", {})
                                  .get("page", "")
                    }
                ]
            }

        return {
            "query": query,
            "results": []
        }

    except Exception as e:
        return {
            "query": query,
            "error": str(e),
            "results": []
        }