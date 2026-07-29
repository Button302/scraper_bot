import json
import copy


watchlist = "config/watchlist.json"

def save_watchlist(data):
    with open(watchlist, "w", encoding="utf-8") as file:
        json.dump(data , file, indent=4, ensure_ascii=False)


def add_to_watchlist():
    is_running = True
    with open(watchlist, "r", encoding="utf-8") as file:
        content = json.load(file)

    while is_running:
        print("----------------------------------------------------------------------------------------------")
        name = input("please enter NAME (ex(it) to exit): ")
        if name in ["ex", "exit"]:
            is_running = False
            break
        print("----------------------------------------------------------------------------------------------")
        max_price = input("please enter MAX PRICE: ")
        print("----------------------------------------------------------------------------------------------")
        min_price = input("please enter MIN PRICE: ")

        search_term_running = True
        search_term = []
        while search_term_running:
            print("----------------------------------------------------------------------------------------------")
            print(f"current search terms list: {search_term}")
            print("----------------------------------------------------------------------------------------------")
            search_term_input = input("please enter SEARCH TERM (ex(it) to exit): ").strip()
            if search_term_input.lower() in ["ex", "exit"]:
                search_term_running = False
            elif search_term_input:
                search_term.append(search_term_input)
        try:
            max_price = int(max_price)
        except ValueError:
            max_price = 0

        try:
            min_price = int(min_price)
        except ValueError:
            min_price = 0

        exclude_running = True
        exclude = []
        while exclude_running:
            print("----------------------------------------------------------------------------------------------")
            print(f"current exclude list: {exclude}")
            print("----------------------------------------------------------------------------------------------")
            exclude_input = input("please enter words to EXCLUDE (ex(it) to exit, space for default): ").strip()
            if exclude_input.lower() in ["ex", "exit"]:
                exclude_running = False
            elif exclude_input == "":
                exclude_default = ["prodano", "Prodano", "Prodáno", "prodáno", "koupím", "koupim", "sháním", "shanim", "poptávám", "poptavam", "poptávka", "poptavka", "výkup", "vykup", "odkoupím", "odkoupim","nefunkční", "nefunkcni", "vadný", "vadny", "poškozený", "poskozeny", "artefakty", "artefakt", "na díly", "na dily", "neoficiální",  "netestováno", "netestovano", "nezkoušeno", "nezkouseno", "bez záruky funkčnosti", "na opravu", "prasklý", "praskly", "spálený", "spaleny", "dárce","pouze krabice", "jen krabice", "prázdná krabice", "prazdna krabice", "krabice od", "obal od", "pouze obal", "box only","výměna", "vymena", "vyměním", "vymenim", "vyměním za", "celá sestava", "cela sestava", "herní pc", "herni pc", "počítačová sestava", "pc sestava", "kompletní pc", "kompletni pc", "nabídněte", "nabidnete", "dohodou", "v textu", "cena dohodou"]
                for word in exclude_default:
                    if not word in exclude:
                        exclude.append(word)
            elif exclude_input:
                exclude.append(exclude_input)

        item = {
                "name": name,
                "search_term": search_term,
                "max_price": max_price,
                "min_price": min_price,
                "exclude": exclude
            }
        content['targets'].append(item)
        save_watchlist(content)
        print("----------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------")
        print(f"saved {name} to watchlist")
        print("----------------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------------")


def search_watchlist():
    is_running = True
    with open(watchlist, "r", encoding="utf-8") as file:
        content = json.load(file)
    targets = content.get('targets', [])
    while is_running:
        print("----------------------------------------------------------------------------------------------")
        answer = input("what are you searching for? (ex(it) for exit): ").strip().lower()
        for target in targets:
            if answer in ['ex', 'exit']:
                is_running = False
            if answer in target['name'].lower():
                print(target['name'])

                search_terms = "" 
                for search_term in target['search_term']:
                    search_terms += search_term + ", "
                print(search_terms)

                print(f"max_price: {target['max_price']}, min_price: {target['min_price']}")

                exclude = ""
                for bad_word in target['exclude']:
                    exclude += bad_word + ", "
                print(exclude)

                print("---------------------------------------")
            
def copy_item():
    with open(watchlist, "r", encoding="utf-8") as file:
        content = json.load(file)

    targets = content.get('targets', [])
    is_running = True
    while is_running:
        print("----------------------------------------------------------------------------------------------")
        answer = input("what would you like to COPY (ex(it) to exit): ").strip()
        if answer.lower() in ["exit", "ex"]:
            is_running = False
            break

        found = False
        for target in targets[:]:
            if answer.lower() == target['name'].lower():
                found = True
                answer_do_you_wanna_delete = input(f"are you sure you want to copy {target['name']} (y(es) n(o)): ")

                if answer_do_you_wanna_delete in ['yes', 'y']:
                    new_name = input(f"what would you like to name the copy name of the old one is {target['name']}")
                    if new_name:
                        new_target = copy.deepcopy(target)
                        new_target['name'] = new_name

                        targets.append(new_target)

                        save_watchlist(content)
                        print(f"target {target['name']} was copied as {new_name}")

                    print(f"{target['name']} was successfully copied")
                else:
                    print(f"action of copying {target['name']} was stopped")

                break
        if not found:
            print(f"no item named {answer} was found in watchlists")



def delete_from_watchlist():
    with open(watchlist, "r", encoding="utf-8") as file:
        content = json.load(file)

    targets = content.get('targets', [])
    is_running = True
    while is_running:
        print("----------------------------------------------------------------------------------------------")
        answer = input("what would you like to DELETE (ex(it) to exit): ").strip()
        if answer.lower() in ["exit", "ex"]:
            is_running = False
            break

        found = False
        for target in targets[:]:
            if answer.lower() == target['name'].lower():
                found = True
                answer_do_you_wanna_delete = input(f"are you sure you want to delete {target['name']} (y(es) n(o)): ")
                if answer_do_you_wanna_delete in ['yes', 'y']:
                    targets.remove(target)
                    save_watchlist(content)
                    print(f"{target['name']} was successfully dealeted")
                else:
                    print(f"action of deleting {target['name']} was stopped")

                break
        if not found:
            print(f"no item named {answer} was found in watchlists")
                    


def print_watchlist():
    with open(watchlist, "r") as file:
        content = json.load(file)
        content = content['targets']
        return content

def edit_watchlist():
    with open(watchlist, "r", encoding="utf-8") as file:
        content = json.load(file)

    targets = content.get('targets', [])
    is_running = True
    is_running_editing = True

    while is_running:
        print("----------------------------------------------------------------------------------------------")
        answer = input("what item would you like to edit? (ex(it) for exit): ").strip().lower()
        if answer in ['ex', 'exit']:
            is_running = False
            break

        found = False
        for target in targets:
            if answer in target['name'].lower():
                found = True
                is_running_editing = True

                while is_running_editing:
                    print()
                    print(f"editing {target['name']}")
                    print()

                    search_terms = "" 
                    for search_term in target['search_term']:
                        search_terms += search_term + ", "
                    print(search_terms)

                    print(f"max_price: {target['max_price']}, min_price: {target['min_price']}")

                    exclude = ""
                    for bad_word in target['exclude']:
                        exclude += bad_word + ", "
                    print(exclude)
                    print()
                    what_to_edit = input("what would you like to edit (ex(it) for exit): ").replace(" ", "_").strip().lower()
                    if what_to_edit == "name":
                        print("----------------------------------------------------------------------------------------------")
                        edit_input = input(f"what do you want to change {target['name']} with: ")
                        if edit_input:
                            target['name'] = edit_input 
                            save_watchlist(content)

                    elif what_to_edit == "search_term":
                        print("----------------------------------------------------------------------------------------------")
                        edit_input = input(f"what would you like to do with {target['search_term']}? (r(move all), a(dd)): ").strip().lower()
                        if edit_input in ["r", "remove"]:
                            target['search_term'] = []
                            save_watchlist(content)
                        elif edit_input in ["a", "add"]:
                            print("----------------------------------------------------------------------------------------------")
                            what_to_add = input(f"what would you like to add to {target['search_term']}?: ")
                            if what_to_add:
                                target['search_term'].append(what_to_add)
                                save_watchlist(content)

                    elif what_to_edit == "max_price":
                        print("----------------------------------------------------------------------------------------------")
                        edit_input = input(f"what do you want to change {target['max_price']} with: ")
                        try:
                            target['max_price'] = int(edit_input) 
                            save_watchlist(content)
                        except ValueError:
                            print("Invalid number price was not changed")

                    elif what_to_edit == "min_price":
                        print("----------------------------------------------------------------------------------------------")
                        edit_input = input(f"what do you want to change {target['min_price']} with: ")
                        try:
                            target['min_price'] = int(edit_input) 
                            save_watchlist(content)
                        except ValueError:
                            print("Invalid number price was not changed")

                    elif what_to_edit == "exclude":
                        print("----------------------------------------------------------------------------------------------")
                        edit_input = input(f"what would you like to do with {target['exclude']}? (r(move all), a(dd)): ").strip().lower()
                        if edit_input in ["r", "remove"]:
                            target['exclude'] = []
                            save_watchlist(content)
                        elif edit_input in ["a", "add"]:
                            what_to_add = input(f"what would you like to add to {target['exclude']}?: ")
                            if what_to_add:
                                target['exclude'].append(what_to_add)
                                save_watchlist(content)

                    elif what_to_edit in ["ex", "exit"]:
                        is_running_editing = False
                break

        if not found:
            print(f"no item matching {answer} was found in watchlist.")


     

def confgure_watchlist():
    is_running = True

    while is_running:
        print("----------------------------------------------------------------------------------------------")
        answer = input("what do you want to do (a(dd), e(dit), c(opy), d(elete), p(rint), s(earch), ex(it)): ")

        if answer == "a" or answer == "add":
            add_to_watchlist()
        elif answer == "e" or answer == "edit":
            edit_watchlist()
        elif answer == "d" or answer == "detele":
            delete_from_watchlist()
        elif answer == "p" or answer == "print":
            content = print_watchlist()
            for item in content:
                exclude = ""
                search_terms = ""

                print(item['name'])

                for term in item['search_term']:
                    search_terms += term + ", "
                print(search_terms)

                print(f"min_price: {item['min_price']}, max_price: {item['max_price']}")

                for word in item['exclude']:
                    exclude += word + ", "
                print(exclude)

                print("----------------------------------------------------------------------------------------------")
        elif answer == "s" or answer == "search":
            search_watchlist()
        elif answer == "ex" or answer == "exit":
            is_running = False
        elif answer in ["c", "copy"]:
            copy_item()
        else:
            print("----------------------------------------------------------------------------------------------")
            print(f"please enter a valid option. {answer} is not a valid option")



if __name__ == '__main__':
    confgure_watchlist()

