import json
import random
import time
from scrappers.bazos import fetch_listings_bazos
from scrappers.sbazar import fetch_listings_sbazar
from notifier import file, send_discord_message

watchlist = "config/watchlist.json"
history = "data/history.json"
while_running = "config/while_running.json"


def write_to_while_running(message, item):
    try:
        with open(while_running, "r", encoding="utf-8") as file:
            content = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        content = {"searched_items": [], "errors": []}
        write_to_history("file error on writing to file", "errors")

    
    content[item] = message

    with open(while_running, "w") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)

def in_watchlist(searching_item):
    se_text = searching_item['text'] 
    title = searching_item['title']
    price = searching_item['price']

    with open(watchlist, "r") as file:
        content = json.load(file)

    with open(while_running, "r") as file2:
        content2 = json.load(file2)
    items_searched = content2['items_searched']
    items_found = content2['items_found']
    items_searched += 1
    write_to_while_running(items_searched, "items_searched")

    watchlist_items = content['targets']


    for item in watchlist_items:
        search_terms = item['search_term']
        bad_words = item['exclude'] + content['default_exclude']
        min_price = item['min_price']
        max_price = item['max_price']

        for bad_word in bad_words:
            for search_term in search_terms:
                if search_term in title:
                    if min_price <= price <= max_price:
                        if bad_word in se_text:
                            items_found += 1
                            write_to_while_running(items_found,"items_found")
                            return True

                    
    return False
                    



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



def run_bot_category():

    with open(watchlist, "r") as file:
        content = json.load(file)
        target = content['categories']
    for category in target:
        formated_category = category.lower()
        bazos_listings = fetch_listings_bazos(formated_category, "category")
        sbazar_listings = fetch_listings_sbazar(formated_category)
        listings = bazos_listings #+ sbazar_listings            
        for listing in listings:
            price = listing['price']
            title = listing['title']
            link = listing['link']
            source = listing['source']
            description = listing.get('description', '')

            full_text = f"{title} {description}".lower()

            message = {"price": price, "title": title, "link": link, "description": description, "source": source}


            listing_info = {"price": price, "title": title, "text": full_text}
            if in_watchlist(listing_info):
                in_history = check_in_history(link)
                if in_history == False:
                    send_discord_message(f"price: {message['price']}, title: {message['title']}, description: {message['description']}, link: {message['link']}", source) 
                    write_to_history(message, "searched_items")

                    print(f"{message['link']}")



def run_bot_single():
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
                bazos_listings = fetch_listings_bazos(formated_term, "single")
                sbazar_listings = fetch_listings_sbazar(formated_term)
                listings = bazos_listings #+ sbazar_listings            
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

is_running = True
while is_running:
    with open(while_running, "r") as file:
        content = json.load(file)
    is_running = content['is_running']
    time_for_loop = content['time_for_loop']
    loops = content['loops']
    time_running = content['time_running']
    time_for_loop += random.randint(1,10)

    run_bot_category()
    loops += 1
    write_to_while_running(loops, "loops")
    time_running += 60
    write_to_while_running(time_running, "time_running")
    time.sleep(time_for_loop)

