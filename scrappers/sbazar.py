import requests

def fetch_listings_sbazar(search_term: str) -> list[dict]:
    url = "https://www.sbazar.cz/api/v1/items/search"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    params = {
            "phrase": search_term,
            "limit": 50,
            "order": "fresh",
            "hide_price_by_agreement": True,
            "radius_precision": 10,
            "locality": "municipality,5740" 
            }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            print(f"sbazar request failed with status code {response.status_code}")
            return []
        data = response.json()
        raw_items = data.get("results", [])
        listings = []
        for item in raw_items:
            title = item.get("name", "")
            price = item.get("price", None)
            seo_url = item.get("seoUrl", "")
            item_id  = item.get("id")
            if seo_url:
                link = f"https://www.sbazar.cz/{seo_url}"
            else:
                 link = f"https://www.sbazar.cz/inzerat/{item_id}"
            description = title
            listings.append(
                    {
                        "title": title,
                        "price": float(price) if price is not None else None,
                        "link": link,
                        "description": description,
                        "source": "sbazar"
                    })
        return listings

    except Exception as e:
            print(f"Error fetching from Sbazar: {e}")
            return []

if __name__ == "__main__":
    listings = fetch_listings_sbazar("nvidia")
    for item in listings[:5]:
        print(f"- {item['title']} | Price: {item['price']} Kč | Link: {item['link']}")
