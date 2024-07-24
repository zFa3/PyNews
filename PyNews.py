import requests, math, datetime

# obtain an API key from
# https://newsapi.org/

API_KEY = "_________________________"
if API_KEY == "_________________________":
    print("INPUT YOUR OWN API KEY!")
API_KEY = input("KEY: ")

page_num = 0
filter_for_dotcom = True

def settings():
    global topic, since_date, articles_per_page, max_articles, response, filter_for_dotcom
    print_banner()
    filter_for_dotcom = True
    topic = input("\033[90mEnter topic: ")
    since_date = (input("\033[90mPublished since (YYYY-MM-DD) (leave empty for last month): "))
    articles_per_page = int(input("\033[90mNumber of articles per page? (Max 25): "))
    max_articles = 25 # the maximum number of articles per page
    articles_per_page = max(min(articles_per_page, max_articles), 5)
    link = f"https://newsapi.org/v2/everything?q={topic}&from={since_date}&sortBy=publishedAt&apiKey={API_KEY}"
    try: response = (requests.get(link).json())["articles"]
    except:
        try:
            if requests.get(link).json()["message"][54] == "You are trying to request results too far in the past.":
                print("---Date is too old!---")
        except:
            print("---Likely invalid parameters!---\n Error code:")
            print(requests.get(link).json())

def settings_advanced():
    global topic, since_date, articles_per_page, max_articles, response, filter_for_dotcom
    print_banner()
    print("\033[92mADVANCED SETTINGS")
    print("\033[90mLeaving things blank is acceptable")
    while True:
        Country = input("\033[90mCountry code (type help to see all codes): ")
        if Country.upper() == "HELP":
            print("ALL CODES:")
            for i in ["ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz", "de", "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us", "ve", "za"]:
                print(i)
        else: break
    topic = input("\033[90mEnter topic: ")
    if topic.upper() == "TOP":
        link = f"https://newsapi.org/v2/top-headlines?country={Country}&apiKey={API_KEY}"
        try: response = (requests.get(link).json())["articles"]
        except:
            try:
                if requests.get(link).json()["message"][54] == "You are trying to request results too far in the past.":
                    print("---Date is too old!---")
            except:
                print("---Likely invalid parameters!---\n Error code:")
                print(requests.get(link).json())
    else:
        while True:
            Category = input("\033[90mCategory (Help for all categories): ")
            if Category.upper() == "HELP":
                print("ALL CATEGORIES:")
                for i in ["science", "sports", "technology", "health", "business", "general", "entertainment"]:
                    print(i)
            else: break
        try: pageSizeInput = int(input("\033[90mnumber of results? (20-100) "))
        except: pageSizeInput = 20
        pageSize = (20 if pageSizeInput not in range(20, 101) else pageSizeInput)
        since_date = input("\033[90mSince (YYYY-MM-DD): ")
        filter_for_dotcom = (True if input("\033[90mInclude only .com sites? (yes/no)").upper() == "YES" else False)
        try: articles_per_page = int(input("\033[90mNumber of articles per page? (Max 25): "))
        except: articles_per_page = 20
        max_articles = 25 # the maximum number of articles per page
        articles_per_page = max(min(articles_per_page, max_articles), 5)
        domains = input("\033[90mDomain to search (url - may return error!)")
        sort_by = input("\033[90mSort results by:\npublishedAt - Publish date\npopularity - Popularity\n")
        link = f"https://newsapi.org/v2/everything?q={topic}&from={since_date}&category={Category}&country={Country}&domains={domains}&sortBy={sort_by}&pageSize={pageSize}&apiKey={API_KEY}"
        try: response = (requests.get(link).json())["articles"]
        except:
            try:
                if requests.get(link).json()["message"][54] == "You are trying to request results too far in the past.":
                    print("---Date is too old!---")
            except:
                print("---Likely invalid parameters!---\n Error code:")
                print(requests.get(link).json())

def print_banner():
    var = 54
    print("\033c\033[91m _______           _     _  _______  _     _  _______ \n|  ____ ||\\     /|| |   | ||  _____|| |   | || ______|\n| |    ||| \\   / ||  \\  | || |      | |   | || |   \n| |____|| \\ \\_/ / |   \\ | || |__    | | _ | || |_____ \n|  _____|  \\   /  | |\\ \\| ||  __|   | || || ||_____  |\n| |         | |   | | \\   || |      | || || |      | |\n| |         | |   | |  \\  || |_____ | || || | _____| |\n|_|         |_|   |_|   |_||_______||_______||_______|\n")
    print("_"*var + "\n\\" + " "*(var - 1) + "/\n/" + "_"*(var - 1) + "\\\n", end = "")
    print("\n")

def printer():
    # Print the response
    try:
        for i in response[page_num * articles_per_page:(page_num + 1) * articles_per_page]:
            # filter for .com only websites, can be turned off in advanced settings ("Advanced")
            if i["source"]["name"] != "[Removed]" or (not (".com" in i["url"]) and filter_for_dotcom):
                print("\033[91m", i["source"]["name"])
                print("\033[92m", i["title"])
                print(i["url"], end = "\n\n")
            else: pass
            # if there is a removed blog post, article, news page,
            # then we will not show it
        print(f"\033[94m -> Page {page_num + 1} out of {math.ceil(len(response)/articles_per_page)}")
    except:
        print(f"ERROR: recieved message:\n{response}")

def help():
    print_banner()
    print("\033[92mPYNEWS - Project made by zFa3 (github.com/zFa3)\n\n\033[90mA Python news app that accesses newsapi.org\nwhich has access to articles published\nby over 150,000 different sources in the last 5 years\nfor current news about various topics\nCommands (non case-sensitive) include\n\n\033[92mNext\033[90m - Next page of results\n\033[92mSettings\033[90m - Opens settings, where you change result parameters\n\033[92mHelp\033[90m - where you are currently at\n\033[92mAdvanced\033[90m - for more advanced settings and fine tuning search results")
    print()


print_banner()
print("Type 'Help' for actions")
action = input("\033[90m>>> ")
# main loop
while True:
    print_banner()
    print("Type 'Help' for actions")
    if action.upper() == "NEXT":
        try:
            page_num += 1; page_num %= math.ceil(len(response)/articles_per_page)
            printer()
        except: print("---No topic was selected!---")
    elif action.upper() == "SETTINGS":
        settings()
        printer()
    elif action.upper() == "HELP":
        help()
    elif action.upper() == "ADVANCED":
        settings_advanced()
        printer()
    action = input("\033[90m>>> ")
