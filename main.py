import json
from scrappers.bazos import fetch_listings_bazos
from scrappers.sbazar import fetch_listings_sbazar
from notifier import send_discord_message

watchlist = "config/watchlist.json"
history = "data/history.json"

def check_in_history(message):
    with open(history, "r") as file:
        content = json.load(file)
        content = content["searched_items"]

        for link in content:
            if message in link['link']:
                return True

        return False


def write_to_history(message, item):
    try:
        with open(history, "r", encoding="utf-8") as file:
            content = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        content = {"searched_items": [], "errors": []}
        write_to_history("file error on writing to file", "errors")

    if item in content and isinstance(content[item], list):
        content[item].append(message)

    else:
        print(f"invalid key '{item}' in history file")
        write_to_history(f"invalid key '{item}' in history file", "errors")
        return

    with open(history, "w") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)



def run_bot():
    with open(watchlist, "r") as file:
        content = json.load(file)
        content = content["targets"]

        for target in content:
            bad_words = target.get("exclude", [])
            max_price = target["max_price"]
            min_price = target["min_price"]
            search_term = target["search_term"]

            if isinstance(search_term, str):
                search_term = [search_term]

            for term in target["search_term"]:
                formated_term = term.replace(" ", "+").lower()
                bazos_listings = fetch_listings_bazos(formated_term)
                sbazar_listings = fetch_listings_sbazar(formated_term)
                listings = bazos_listings + sbazar_listings            
                for listing in listings:
                    price = listing['price']
                    title = listing['title']
                    link = listing['link']
                    source = listing['source']
                    description = listing.get('description', '')

                    full_text = f"{title} {description}".lower()

                    if any(word.lower() in full_text for word in bad_words):
                        continue

                    message = {"price": price, "title": title, "link": link, "description": description, "source": source}

                    if price != None:
                        if price <= max_price and price >= min_price:
                            in_history = check_in_history(link)
                            if in_history == False:
                                send_discord_message(f"price: {message['price']}, title: {message['title']}, description: {message['description']}, link: {message['link']}", source) 
                                write_to_history(message, "searched_items")
                                print(f"{message['link']}")
                    else:
                        print("Price not found")

run_bot()
