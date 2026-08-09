import re
import feedparser

def parse_rss_listing(rss_title: str) -> dict:
    parts = rss_title.rsplit(":", 1)
    
    if len(parts) < 2:
        return {"title": rss_title.strip(), "price": None, "condition": "N/A"}

    raw_title = parts[0].strip()
    raw_price_str = parts[1].strip()

    # Clean out normal spaces and non-breaking spaces (\xa0)
    clean_number_str = re.sub(r'[\s\xa0]+', '', raw_price_str)

    if clean_number_str.isdigit():
        price = int(clean_number_str)
        condition = None
    else:
        price = None
        condition = raw_price_str

    return {
        "title": raw_title,
        "price": price,
        "condition": condition
    }

def fetch_listings_bazos(search_term: str, mode: str) -> list[dict]:
    if mode == "single":
        url = f"https://www.bazos.cz/rss.php?hlokalita=60200&humkreis=25&hledat={search_term}"
        rss_feed = feedparser.parse(url)
        listings = []

        for entry in rss_feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            description = entry.get("description", "")
            
            
            data = parse_rss_listing(title)
            data["link"] = link
            data["description"] = description
            data["source"] = "bazos"
            listings.append(data)
            
        return listings
    elif mode == "category":
        url = f"https://www.bazos.cz/rss.php?rub={search_term}&hlokalita=60200&humkreis=15"
        rss_feed = feedparser.parse(url)
        listings = []

        for entry in rss_feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            description = entry.get("description", "")
            
            
            data = parse_rss_listing(title)
            data["link"] = link
            data["description"] = description
            data["source"] = "bazos"
            listings.append(data)
            
        return listings
    return []


if __name__ == "__main__":
    test_url = "https://www.bazos.cz/rss.php?rub=pc"
    results = fetch_listings_bazos(test_url, "single")
    
    for item in results:
        print(item)
