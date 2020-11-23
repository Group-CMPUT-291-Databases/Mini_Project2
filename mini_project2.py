import pymongo, os
from datetime import date

#Phase 2 portions should be put into here
def main():
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
    #User ID get here
    #ID is optional
    currentUser = None
    u = input("Enter user ID or type skip: ")
    if u.lower() == "skip":
        currentUser = None
    else:
        currentUser = u
    
    if currentUser != None:
        posts = db["Posts"]
        returns = posts.find({"OwnerUserId":currentUser})
        avgScore = 0
        count = 0
        for post in returns:
            if post["PostTypeId"] == "1":
                count += 1
                avgScore += post["Score"]
    
        if avgScore == 0:
            avgScore = 1
        print("Question Count: ",count)
        print("Average Question Score: ",(avgScore/count))
if __name__ == "__main__":
    main()