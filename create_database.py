import pymongo, json, os

#This file creates the database on the specified port
#This file must be run first to populate and create the database
#This file is only for Phase 1
#
def phase1():
    currentDirec = os.getcwd()

    postPath = currentDirec + "/Posts.json"
    with open(postPath) as postFile:
        posts = json.load(postFile)
    tagsPath = currentDirec + "/Tags.json"
    with open(tagsPath) as tagsFile:
        tags = json.load(tagsFile)
    votesPath = currentDirec + "/Votes.json"
    with open(votesPath) as votesFile:
        votes = json.load(votesFile)

    #Verify here port is a valid port
    found = False
    while found != True:
        port = input("Input port used for connection: ")
        fullPort = "mongodb://localhost:" + port
        if len(port) != 5:
            print("Not a valid port number")
        else:
            found = True

    print(fullPort)
    client = pymongo.MongoClient(fullPort)
    db = client["291db"]

    collist = db.list_collection_names()
    print(collist)
    Posts = db["Posts"]
    Tags = db["Tags"]
    Votes = db["Votes"]
    if "Posts" in collist:
        Posts.delete_many({})
    if "Votes" in collist:
        Votes.delete_many({})
    if "Tags" in collist:
        Tags.delete_many({})

    #print(posts['posts']['row'][1])
    Posts.insert_many(posts['posts']['row'])
    Tags.insert_many(tags['tags']['row'])
    Votes.insert_many(votes['votes']['row'])

def main():
    phase1()
    
if __name__ == "__main__":
    main()