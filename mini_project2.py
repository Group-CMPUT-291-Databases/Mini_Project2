import pymongo, os, sys
from datetime import date
from pymongo import MongoClient

currentUser = ''
current_id = None
Posts = None
Tags = None
Votes = None

def search_for_questions():
    global Posts, Tags, Votes, current_id, currentUser

    keyword_input = input("Type the keywords separated by comma and no spaces: ")
    keyword_list = keyword_input.split(",")

    search_result_array = []
    for keyword in keyword_list:
        print(keyword)
        results = Posts.find({"$or":[
            {"PostTypeId": "1","Body": {"$regex":".*"+keyword+".*"} },
            {"PostTypeId":"1", "Title": {"$regex":".*"+keyword+".*"}},
            {"PostTypeId":"1", "Tags": {"$regex":".*"+keyword+".*"}}

            ]})
        for result in results:
            search_result_array.append(result.copy())

    counter = 1
    if len(search_result_array) == 0:
        print("No results found")
        return
    for result in search_result_array:
        print("Result: ",str(counter))
        print("Title: ",result["Title"])
        print("CreationDate: ",result["CreationDate"])
        print("Score: ",result["Score"])
        print("AnswerCount: ",result["AnswerCount"],"\n")
        counter += 1

    input_post = input("Input the Result Number to select the post: ")
    correct_input = False

    while correct_input == False:
        try:
            input_post = int(input_post)
            
            if input_post > 0 and input_post <= len(search_result_array)+1:
                #{"Id": search_result_array[input_post-1]["Id"]}
                Posts.update_one({"Viewcount":""}, {"$inc":{"ViewCount": 1}})
                correct_input = True
                action_answer_input= input("Do you want to answer this question? [y for yes and anything else for no] ")
                if action_answer_input == "y":
                    question_action_answer(search_result_array[input_post-1]["Id"])

                return search_result_array[input_post-1]["Id"]
        
            else:
                print("Post does not exist, try again")
                input_post = input("Input the Result Number to select the post: ")


        except: 
            print("Wrong Input")
            input_post = input("Input the Result Number to select the post: ")

def post_a_question():
    global Posts, Tags, Votes, current_id, currentUser

    input_title= input("Title text: ")
    input_body_text = input("Body text: ")
    input_tags = input("Add zero or more tags in this format - <hardware><mac><powerpc><macos>")



    new_post = { 
    "Id": str(int(current_id)+1),
    "PostTypeId": "1",
    "CreationDate": date.today(),
    "Score": 0,
    "ViewCount": 0,
    "Body": input_body_text,
    "OwnerUserId": currentUser,
    "Title": input_title,
    "Tags": input_tags,
    "AnswerCount": 0,
    "CommentCount": 0,
    "ContentLicense": "CC BY-SA 2.5" 

    }
    current_id = str(int(current_id)+1)

    Post.insert_one(new_post)

#Phase 2 portions should be put into here
def main():
    global Posts, Tags, Votes, current_id, currentUser

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
    Posts = db['Posts']
    Tags = db['Tags']
    Votes = db['Votes']
    #cursor Id
    #cursor_id = Posts.find().sort( "Id", -1 ).limit(1)
    cursor_id = Posts.find_one({"$query":{},"$orderby":{"_id":-1}})
    current_id = cursor_id["Id"]
    print(current_id)
    #User ID get here
    #ID is optional
    u = input("Enter user ID or type skip: ")
    if u.lower() == "skip":
        currentUser = ''
    else:
        currentUser = u
    
    if currentUser != '':
        returns = Posts.find({"OwnerUserId":currentUser})
        returnedVotes = Votes.find({"UserId":currentUser})
        qAvgScore = 0
        aAvgScore = 0
        qcount = 0
        acount = 0
        vcount = 0
        for post in returns:
            if post["PostTypeId"] == "1":
                qcount += 1
                qAvgScore += int(post["Score"])
            if post["PostTypeId"] == "2":
                acount += 1
                aAvgScore += int(post["Score"])
        #Not the best way to count, but .count() keeps giving warnings
        for vote in returnedVotes:
            vcount += 1
    
        print("Question Count: ",qcount)
        if qcount == 0:
            print("Average Question Score: ",(qAvgScore))
        else:
            print("Average Question Score: ",(qAvgScore/qcount))
        print("Answer Count: ",acount)
        if acount == 0:
            print("Average Answer Score: ",(aAvgScore))
        else:
            print("Average Answer Score: ",(aAvgScore/acount))
        print("Number of votes casted: ",vcount)
    loop = True
    while loop != False:
        print("\n","Main Selection Menu")
        print("Type 'search question' to search for a question")
        print("Type 'post question' to post a question")
        menu = input()
        if menu.lower() == "search question":
            questions = search_for_questions()
        elif menu.lower() == "post question":
            post_a_question()
        elif menu.lower() == 'quit':
            sys.exit()


if __name__ == "__main__":
    main()