import requests

# obtain an API key from
# https://newsapi.org/ 
API_KEY = "API_KEY" # INPUT API KEY HERE
# ascii title
print("\033[91m _______           _     _  _______  _     _  _______ \n|  ____ ||\\     /|| |   | ||  _____|| |   | || ______|\n| |    ||| \\   / ||  \\  | || |      | |   | || |   \n| |____|| \\ \\_/ / |   \\ | || |__    | | _ | || |_____ \n|  _____|  \\   /  | |\\ \\| ||  __|   | || || ||_____  |\n| |         | |   | | \\   || |      | || || |      | |\n| |         | |   | |  \\  || |_____ | || || | _____| |\n|_|         |_|   |_|   |_||_______||_______||_______|\n")

topic = input("Enter topic: ")
since_date = input("Since (YYYY-MM-DD): ")
link = f"https://newsapi.org/v2/everything?q={topic}&from={since_date}&sortBy=publishedAt&apiKey={API_KEY}"
response = requests.get(link)

# Print the response
response = (response.json())
for i in response["articles"]:
    print(i["source"]["name"])
    print(i["title"])
    print(i["url"])
