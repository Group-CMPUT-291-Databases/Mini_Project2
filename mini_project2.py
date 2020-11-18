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
if __name__ == "__main__":
    main()