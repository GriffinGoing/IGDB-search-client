import requests
import datetime
"""
Greetings, sire! Tis I, your lowly programming knave! As you requested, this program uses an API to search a selected category for a term in a specific API, and give you data as such. This seems quite important to the rule of a kingdom, and I am thusly honored by your holiest of opportunities to have embarked on this jovial journey!

Author: Griffin Going
ASCII Art by: maybe Joan G. Stark, not sure, the signature wasn't present

"""

#Global variables, RIP Nic Cage


# my api key
myKey = "346aa2b5d513be0144890c391e82b515"

    
# base URL to build from. includes games endpoint 
baseURL = "https://api-v3.igdb.com/games/"
    
# url for alt names
altURL = "https://api-v3.igdb.com/alternative_names"

#finesse the dict
HEADER = { 'user-key': myKey, 'content-type': 'application/json', 'fields': "*" } 

def getCategory():
    print("If you'd be so kind as to enter the category you'd like to search in: ")
    category = input()
    return category

"""
method to get the term the user wishes to search for
"""
def getTerm():
    print("Now, my liege, you must tell u the term you'd like to search for: ")
    searchTerm = input()
    return searchTerm

def main():
 

    print("#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~")
    print("""             
               ,'   ,`-.
    |.        /     |\  `.
    \ \      (  ,-,-` ). `-._ __
     \ \      \|\,'     `\  /'  `\\
      \ \      ` |, ,  /  \ \     \\
       \ \         `,_/`, /\,`-.__/`.
        \ \            | ` /    /    `-._
         \\\           `-/'    /         `-.
          \\\`/ _______,-/_   /'             \\
         ---'`|       |`  ),' `---.  ,       |
          \..-`--..___|_,/          /       /
                     |    |`,-,...,/      ,'     
                     \    | |_|   /     ,' __  r-'',
                      |___|/  |, /  __ /-''  `'`)  |  
                   _,-'   ||__\ /,-' /     _,.--|  (
                .-'       )   `(_   / _,.-'  ,-' _,/
                 `-------'       `--''       `'''""")
    print("*********************************************************")
    print("Greetings, sire! Welcome to the ****AMAZING GAME-FINDER 6000****")
    
    while(True):
        search()

    """ 
    # The following code queries the user for a search endpoint. superfluous since we're searching game names

    # get the search category
    category = getCategory()
    """
    
def search():
    #get the search term
    searchTerm = getTerm()

    print("***The wizard in the box before you whirs, zips, and mumbles as it searches for results containing \"" + searchTerm + "\"...***")   

    gameRequest = requests.post(baseURL, data='search "' + searchTerm + '";', headers = HEADER)
    statusCode = gameRequest.status_code

    print("Status Code of Request: ", end = '') 
    print(statusCode)
    print("\n")

    if(statusCode != 200): 
        #handle shit
        print("BAD")

    data = gameRequest.json()
    print(data)
    
    """
    for game in data:
        print(game['id'])
        r = requests.post(baseURL, data='fields *; where id='+str(game['id'])+';', headers = HEADER)
        thisGame = r.json()
        print(thisGame)
    """
    
    gameCounter = 1 #to use as index, subtract 1
    for game in data:
        r = requests.post(baseURL, data='fields *; where id='+str(game['id'])+';', headers = HEADER)
        thisGame = r.json()
        print(str(thisGame[0]['id']) + ". " + thisGame[0]['name'])
        gameCounter = gameCounter + 1
        
        if ('alternative_names' in thisGame[0].keys()):
            for altId in thisGame[0]['alternative_names']:
                altRequest = requests.post(altURL, data='fields *; where id='+str(altId)+';', headers = HEADER)
                altGame = altRequest.json()
                try:
                    print("  - " + altGame[0]['name'])
                except:
                    print("<returned empty list>")

    print("Enter an ID number for more info, 0 for a new search. Press any other key(s) to quit: ")
    selection = input()

    #if input is not an integer, exit
    try:
        selection = int(selection)
    except:
        quit()
    

    if (selection != 0 and (selection in data)):
        chosenReq = requests.post(baseURL, data = 'fields *; where id='+str(selection)+';', headers = HEADER)
        chosenGame = chosenReq.json()
        print("**********************************************")
        print(chosenGame[0]['name'])
        print("Category: " + lookupCategory(chosenGame[0]['category']))

        try:
            print(chosenGame[0]['dlcs'])
        except:
            print("No DLC")
        
        try:
            print(chosenGame[0]['expansions'])
        except:
            print("No expansions")

        print("First Release: " + getTime(chosenGame[0]['first_release_date']))
        
        try:
            print(chosenGame[0]['game_engines'])
        except:
            print("Game Engines not available")

        print(chosenGame[0]['genres'])
        print("Rating: " + str(chosenGame[0]['rating']))
        print("Summary: " + chosenGame[0]['summary'])
        print("**********************************************")


def lookupCategory(catNum):
    categories = ["Main Game", "DLC AddOn", "Expansion", "Bundle", "Standalone Expansion", "Mod", "Episode"]
    return categories[catNum]

def lookupDLC(dlcArray):
    for id in dlcArray:
        return 0


def getTime(unixTime):
    time = datetime.datetime.fromtimestamp(int(unixTime)).strftime('%Y-%m-%d %H:%M:%S')
    return time

def quit():
    print("*** O K A Y  B Y E E E ***")
    exit(0)

if __name__ == "__main__":
    main()



