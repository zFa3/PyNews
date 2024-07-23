import requests, math

# obtain an API key from
# https://newsapi.org/

API_KEY = "__________________" # INPUT YOUR API KEY HERE
page_num = 0

def settings():
    global topic, since_date, articles_per_page, max_articles, response
    print("\033c\033[91m _______           _     _  _______  _     _  _______ \n|  ____ ||\\     /|| |   | ||  _____|| |   | || ______|\n| |    ||| \\   / ||  \\  | || |      | |   | || |   \n| |____|| \\ \\_/ / |   \\ | || |__    | | _ | || |_____ \n|  _____|  \\   /  | |\\ \\| ||  __|   | || || ||_____  |\n| |         | |   | | \\   || |      | || || |      | |\n| |         | |   | |  \\  || |_____ | || || | _____| |\n|_|         |_|   |_|   |_||_______||_______||_______|\n")
    topic = input("Enter topic: ")
    since_date = input("Since (YYYY-MM-DD): ")
    articles_per_page = int(input("Number of articles per page? (Max 25): "))
    max_articles = 25 # the maximum number of articles per page
    articles_per_page = max(min(articles_per_page, max_articles), 5)
    link = f"https://newsapi.org/v2/everything?q={topic}&from={since_date}&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(link).json()["articles"]
    print("\n\n\n")

def printer():
    # Print the response
    try:
        for i in response[page_num * articles_per_page:(page_num + 1) * articles_per_page]:
            if i["source"]["name"] != "[Removed]":
                print("\033[91m", i["source"]["name"])
                print("\033[92m", i["title"])
                print(i["url"], end = "\n\n")
            else: pass
            # if there is a removed blog post, article, news page,
            # then we will not show it
        print(f"\033[94m -Page #{page_num + 1} out of {math.ceil(len(response)/articles_per_page)}")
    except:
        print(f"ERROR: recieved message:\n{response}")


# main loop

settings()
printer()
print("Type 'Help' for actions")

while True:
    action = input(">>>")
    if action.upper() == "NEXT":
        page_num += 1; page_num = min(math.ceil(len(response)/articles_per_page), page_num)
        printer()
    elif action.upper() == "SETTINGS":
        settings()
    elif action.upper() == "HELP":
        help()
