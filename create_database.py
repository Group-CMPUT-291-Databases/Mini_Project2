import pymongo, json, os, time

#This file creates the database on the specified port
#This file must be run first to populate and create the database
#This file is only for Phase 1
#
start_time = None
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
        fullPort = "mongodb://localhost:" + str(port)
        if len(port) != 5:
            print("Not a valid port number")
        else:
            found = True

    print(fullPort)
    client = pymongo.MongoClient(fullPort)
    db = client["291db"]

    collist = db.list_collection_names()
    print("Post connection successful")
    Posts = db["Posts"]
    Tags = db["Tags"]
    Votes = db["Votes"]
    if "Posts" in collist:
        Posts.delete_many({})
    if "Votes" in collist:
        Votes.delete_many({})
    if "Tags" in collist:
        Tags.delete_many({})

    #print(type(posts['posts']['row'][0]))
    #Fix terms having <p> or </p>
    #Remove punctuations
    for d in posts['posts']['row']:
        d['terms'] = []
        for word in d['Body'].split():
            word = removePunc(word)
            if word in d['terms']:
                continue
            if len(word) >= 3:
                d['terms'].append(word.lower())
        if "Title" in d.keys():
            for word in d["Title"].split():
                word = removePunc(word)
                if word in d['terms']:
                    continue
                if len(word) >= 3:
                    d['terms'].append(word.lower())
        if "Tags" in d.keys():
            for word in d["Tags"].split('><'):
                temp = removePunc(word)
                if temp in d['terms']:
                    continue
                if len(temp) >= 3:
                    d['terms'].append(temp.lower())               
    Posts.insert_many(posts['posts']['row'])
    Tags.insert_many(tags['tags']['row'])
    Votes.insert_many(votes['votes']['row'])

    Posts.create_index([('terms', 1)])

def removePunc(word):
    newWord = word.replace('<p>','')
    newWord = newWord.replace('</p>','')
    newWord = newWord.replace('<','')
    newWord = newWord.replace('>','')
    newWord = newWord.replace('?','')
    newWord = newWord.replace('.','')
    newWord = newWord.replace('!','')
    return newWord
def main():
    start_time = time.time()
    phase1()
    print(time.time()-start_time)
    
if __name__ == "__main__":
    main()