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
    
    print("*********************************")
    print("Status Code of Request: " + str(statusCode)) 
    print("*********************************")

    if(statusCode != 200): 
        #handle shit
        print("BAD")

    data = gameRequest.json()
    #print(data)
    
    """
    for game in data:
        print(game['id'])
        r = requests.post(baseURL, data='fields *; where id='+str(game['id'])+';', headers = HEADER)
        thisGame = r.json()
        print(thisGame)
    """
    
    for game in data:
        r = requests.post(baseURL, data='fields *; where id='+str(game['id'])+';', headers = HEADER)
        thisGame = r.json()
        print(str(thisGame[0]['id']) + ". " + thisGame[0]['name'])
        
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
    
    selectionIsOption = False

    for game in data:
        #print(game)
        if (selection == game['id']):
            selectionIsOption = True

    if (selection != 0 and selectionIsOption):
        chosenReq = requests.post(baseURL, data = 'fields *; where id='+str(selection)+';', headers = HEADER)
        chosenGame = chosenReq.json()
        #print(chosenGame)
        print("**********************************************")
        print(chosenGame[0]['name'])
        print("Category: " + lookupCategory(chosenGame[0]['category']))
        
        print("DLC:")
        try:
            for game in chosenGame[0]['dlcs']:
                #print (game)
                lookupDLC(str(game))
        except:
            print(" - no dlc")
        
        print("Expansions: ")
        try:
            #print(chosenGame[0]['expansions'])
            for game in chosenGame[0]['expansions']:
                lookupDLC(str(game))
        except:
            print(" - no expansions")

        print("First Release: " + getTime(chosenGame[0]['first_release_date']))
       
        print("Game Engines: ")
        try:
            #print(chosenGame[0]['game_engines'])
            for engine in chosenGame[0]['game_engines']:
                lookupGameEngine(str(engine), True)
        except:
            print(" -   not available")
        
        print("Genres: ")
        #print(chosenGame[0]['genres'])
        try:
            for platform in chosenGame[0]['genres']:
                lookupGameEngine(str(platform), False)
        except:
            print(" -   not available")

        print("Rating: " + str(chosenGame[0]['rating']))
        print("Summary: " + chosenGame[0]['summary'])
        print("**********************************************")
        
    elif(selection != 0 and not selectionIsOption):
        print("That ID is not from the above selection. Beginning new search...")

"""
Method for looking up game engines and platforms. Can easily be adapted via the use of a dictionary to change the URL.
Originally for looking up gaming engines exclusively, but hey, abstracting and all. Name is due for a refactor.
Accepts the ID to look up and a boolean parameter (true for engine, false for genres). Should change boolean to key values
for a dictionary, but such a thing would take time and this is due.
"""
def lookupGameEngine(lookupId, engine):
    if (engine):
        lookupURL = "https://api-v3.igdb.com/game_engines"
    else:
        lookupURL = "https://api-v3.igdb.com/genres"
    r = requests.post(lookupURL, data = 'fields *; where id='+lookupId+';', headers = HEADER)
    data = r.json()
    print(" -   " + data[0]['name'])

"""
method to look up the corresponding value from the IGDB category enum to the category number.
Parameters: catNum - the category number
"""
def lookupCategory(catNum):
    categories = ["Main Game", "DLC AddOn", "Expansion", "Bundle", "Standalone Expansion", "Mod", "Episode"]
    return categories[catNum]

"""
Comparable to other lookup methods, this accepts the dlc id and prints the corresponding dlc name.
"""
def lookupDLC(dlcId):
    r = requests.post(baseURL, data = 'fields *; where id='+dlcId+';', headers = HEADER)
    dlc = r.json()
    #print(dlc)
    print(" -   " + dlc[0]['name'])

"""
method serving to help readable in the main function. Converts a unxi time stamp to readable format.
Parameters: unixTime, a unix time stamp
"""
def getTime(unixTime):
    time = datetime.datetime.fromtimestamp(int(unixTime)).strftime('%Y-%m-%d %H:%M:%S')
    return time

"""
Does what it say. Quits.
"""
def quit():
    print("*** O K A Y  B Y E E E ***")
    exit(0)

if __name__ == "__main__":
    main()



