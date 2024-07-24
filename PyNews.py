import requests, math

# obtain an API key from
# https://newsapi.org/

API_KEY = input("API KEY: ")
# we start on page 1 (which is index 0)
page_num = 0
filter_for_dotcom = True

def settings():
    # settings all variables to global, since the program is split into multiple functions
    global topic, since_date, articles_per_page, max_articles, response, filter_for_dotcom
    # removing unneccessary code, having print_banner as one function reduces # of lines
    print_banner()
    # Filter for .com sites is automatically set to true
    filter_for_dotcom = True
    ###### Input all the parameters ######
    topic = input("\033[90mEnter topic: ")
    since_date = (input("\033[90mPublished since (YYYY-MM-DD) (leave empty for last month): "))
    articles_per_page = int(input("\033[90mNumber of articles per page? (Max 25): "))
    max_articles = 25 # the maximum number of articles per page
    articles_per_page = max(min(articles_per_page, max_articles), 5)
    link = f"https://newsapi.org/v2/everything?q={topic}&from={since_date}&sortBy=publishedAt&apiKey={API_KEY}"
    # try to request data from https://newsapi.org, if it fails we catch the error and inform the user
    try: response = (requests.get(link).json())["articles"]
    except:
        try:
            if requests.get(link).json()["message"][54] == "You are trying to request results too far in the past.":
                # this means we are trying to look for things too far in the past
                # because we are using the free version of newsAPI, we only
                # have a window of about 1 month ago
                print("---Date is too old!---")
        except:
            # other errors means likely user fault or
            # internet issues, in this case its more useful to
            # return the whole error
            print("---Likely invalid parameters!---\n Error code:")
            print(requests.get(link).json())

def settings_advanced():
    countries = ["ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz", "de", "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us", "ve", "za"]
    # the advanced settings are similar to the regular ones, but with more options
    global topic, since_date, articles_per_page, max_articles, response, filter_for_dotcom
    print_banner()
    print("\033[92mADVANCED SETTINGS")
    print("\033[90mLeaving things blank is acceptable")
    # leaving things blank will just default to the website's defualt,
    # rather than inputting them ourselves
    while True:
        # repeatedly ask for a country code until the user
        # gives a valid code
        Country = input("\033[90mCountry code (type help to see all codes): ")
        if Country.upper() == "HELP":
            print("ALL CODES:")
            for i in countries:
                print(i)
        # if and only if the code is valid, we continue
        elif Country in countries: break
    topic = input("\033[90mEnter topic: ")
    # if the input is "top" then we return the top headlines
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
        domains = input("\033[90mDomain to search (url - may return error!)") # say we wanted to only search wsj.com (wall street journal), we can do that
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
    # since we print the banner multiple times, I made a function that can be called
    # to print the ascii art
    var = 54
    print("\033c\033[91m _______           _     _  _______  _     _  _______ \n|  ____ ||\\     /|| |   | ||  _____|| |   | || ______|\n| |    ||| \\   / ||  \\  | || |      | |   | || |   \n| |____|| \\ \\_/ / |   \\ | || |__    | | _ | || |_____ \n|  _____|  \\   /  | |\\ \\| ||  __|   | || || ||_____  |\n| |         | |   | | \\   || |      | || || |      | |\n| |         | |   | |  \\  || |_____ | || || | _____| |\n|_|         |_|   |_|   |_||_______||_______||_______|\n")
    print("_"*var + "\n\\" + " "*(var - 1) + "/\n/" + "_"*(var - 1) + "\\\n", end = "")
    print("\n")

def printer():
    # Print the articles and their urls
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
    print("\033[92mPYNEWS - Project made by zFa3 (github.com/zFa3)\n\n\033[90mA Python news app that accesses newsapi.org\nwhich has access to articles published\nby over 150,000 different sources in the last 5 years\nfor current news about various topics\nCommands (non case-sensitive) include\n\n\033[92mNext\033[90m - Next page of results\n\033[92mSettings\033[90m - Opens settings, where you change result parameters\n\033[92mHelp\033[90m - where you are currently at\n\033[92mAdvanced\033[90m - for more advanced settings and fine tuning search results\n\033[92mCredits\033[90m - made possible thanks to newsapi.org!")
    print()


print_banner()
print("Type 'Help' for actions")
action = input("\033[92m>>> ")
# main loop, since the user can ask for multiple topics, multiple times
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
    elif action.upper() == "CREDITS":
        print("\033c \033[92m-> \033[90mAll code written by me (zFa3) in Python, free to use\nmade with the free version of newsapi\nlocated at https://newsapi.org")
    action = input("\033[92m>>> ")
