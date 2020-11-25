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

    correct_input = False

    while correct_input == False:

            input_post = input("Input the Result Number to select the post: ")

            if input_post.isnumeric():
                input_post = int(input_post)
                if (input_post > 0 and input_post <= len(search_result_array)):
                    #{"Id": search_result_array[input_post-1]["Id"]}
                    Posts.update_one({"Viewcount":""}, {"$inc":{"ViewCount": 1}})
                    correct_input = True
                    action_answer_input= input("Do you want to answer this question? [y for yes and anything else for no] ")
                    if action_answer_input == "y":
                        question_action_answer(search_result_array[input_post-1]["Id"])

                    return search_result_array[input_post-1]["Id"]
        
                else:
                    print("Post does not exist, try again")
            else:
                print("Not a valid post selection")




def post_a_question():
    global Posts, Tags, Votes, current_id, currentUser

    input_title= input("Title text: ")
    input_body_text = input("Body text: ")
    input_tags = input("Add zero or more tags in this format - <hardware><mac><powerpc><macos>")



    new_post = { 
    "Id": str(int(current_id)+1),
    "PostTypeId": "1",
    "CreationDate": str(date.today()),
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

    Posts.insert_one(new_post)

def question_action_answer(question_id):
    global Posts, Tags, Votes, current_id, currentUser
    
    input_body_text = input("Body text:")
    



    new_post = { 
    "Id": str(int(current_id)+1),
    "PostTypeId": "2",
    "ParentId": question_id,
    "CreationDate": str(date.today()),
    "Score": 0,
    "ViewCount": 0,
    "Body": input_body_text,
    "OwnerUserId": currentUser,
    "AnswerCount": 0,
    "CommentCount": 0,
    "ContentLicense": "CC BY-SA 2.5" 

    }

    current_id = str(int(current_id)+1)

    Posts.insert_one(new_post)


def list_answers(db,search_postID):
    #Print all answers related to the question
    answers_table = db["Posts"]
    test_post = answers_table.find({"Id": search_postID})
    
    for postid in test_post:
        postID = postid["Id"]
        accepted_id = postid["AcceptedAnswerId"]
        scoreNum = postid["Score"]
    primary_list = answers_table.find({"ParentId": postID})
    answers_to_print = []
    
    #If an answer is marked as the accepted answer, it must be shown as the first answer and should be marked with a star. 
    for answer in primary_list:
        answerID = answer["Id"]
        if answerID == accepted_id:
            print("*",end = '' )
            answers_to_print.insert(0, answer)
            
        else:
            answers_to_print.append(answer)
    #display the first 80 characters of the body text (or the full text if it is of length 80 or less characters)
    counter = 0
    for item in answers_to_print:
        body_text = item["Body"]
        cr_date = item[ "CreationDate"]
        ans_score = item["Score"]
        if len(body_text)> 80:
            print(counter,end = ', ' )
            print("Body: " ,end = '')
            print(body_text[:80] ,end = ', ' )
            print("CreationDate: ", end = '' )
            print(cr_date,end = ', ')
            print("Score: ",end = '' )
            print(ans_score)
            counter= counter + 1
        else:
            print(counter,end = ', ' )
            print("Body: " ,end = '')
            print(body_text ,end = ', ' )
            print("CreationDate: ", end = '' )
            print(cr_date,end = ', ')
            print("Score: ",end = '' )
            print(ans_score)     
            
    input_answer = input("Input the Answer Number to select the answer: ")
    correct_input = False
    
    while correct_input == False:
        input_answer = int(input_answer)
        
        if input_answer >= 0 and input_answer <= len(answers_to_print)+1:
            print(answers_to_print[input_answer])
            correct_input = True
            add_vote(postID,answerID,db,scoreNum)

        else:
            print("Post does not exist, try again")
            input_answer = input("Input the Result Number to select the post: ")
            
def add_vote(postID,answerID, db,scoreNum):
    global current_id, currentUser
    #Retreive the last vote ID in ordeer to create a new one
    votes_table = db["Votes"]
    votes_list = votes_table.find()
    vote_id_list = []
    for vote_id in votes_list:
        vote_id_list.append(vote_id["Id"])
    vote_id_list.sort(key = int)
    last_vote_id = int(vote_id_list[len(vote_id_list)-1]) + 1
    #check if the user has voted on a post

    new_score = int(scoreNum) +1
    add_vote_loop = False
    while add_vote_loop == False:
        answer_action_input= input("Do you want to add a vote to the selected question/ answer ? [y for yes and anything else for no]")
        has_voted = False
        voted_check = votes_table.find({"UserId": currentUser})
        for vote in voted_check:
            if postID == vote["PostId"]:
                has_voted = True
                
        #ask if the vote is for the question or the answer
        if answer_action_input == "y":
            vote_type = input("Enter 'question' to vote on a question or Enter 'answer' to vote on an answer : ")
            if has_voted == True and check_user_anonymous(currentUser,db) == False:
                print("Sorry you have already voted on this post")
                add_vote_loop = True
            #if the use is anonymous
            if check_user_anonymous(currentUser,db) == True:
                if vote_type == 'question':
                    question_vote = { 
                        "Id": str(last_vote_id),
                        "PostId": postID,
                        "VoteTypeID": "2",
                        "CreationDate": str(date.today()),
                    
                        }
                    last_vote_id = str(int(last_vote_id)+1)
                    
                    votes_table.insert_one(question_vote)  
                    print("Vote has been added ")
                elif vote_type == 'answer':
                    question_vote = { 
                        "Id": str(last_vote_id),
                        "PostId": answerID,
                        "VoteTypeID": "2",
                        "CreationDate": str(date.today()),
                    
                        }
                    last_vote_id = str(int(last_vote_id)+1)
                    
                    votes_table.insert_one(question_vote)   
                    print("Vote has been added")
                    
                add_vote_loop = True
            #if the user is not anonymus update userID
            elif check_user_anonymous(currentUser,db) == False:
                if vote_type == 'question':
                    question_vote = { 
                        "Id": str(last_vote_id),
                        "PostId": postID,
                        "UserId": currentUser,
                        "VoteTypeID": "2",
                        "CreationDate": str(date.today()),
                    
                        }
                    last_vote_id = str(int(last_vote_id)+1)
                    
                    votes_table.insert_one(question_vote)
                    print("Vote has been added")
           
                elif vote_type == 'answer':
                    question_vote = { 
                        "Id": str(last_vote_id),
                        "PostId": answerID,
                        "UserId": currentUser,
                        "VoteTypeID": "2",
                        "CreationDate": str(date.today()),
                    
                        }
                    last_vote_id = str(int(last_vote_id)+1)
                    
                    votes_table.insert_one(question_vote)
                    ("Vote has been added")
                    
                add_vote_loop = True                
                
        else:
            continue

def check_user_anonymous(currentUser,db):
    checking = db['Posts']
    is_anonymous = False
    anonymous_post = checking.find({"Id": ""})
    for user in anonymous_post:
        if user == currentUser:
            is_anonymous =  True 
        else:
            is_anonymous = False
    return is_anonymous

#Phase 2 portions should be put into here
def main():
    global Posts, Tags, Votes, current_id, currentUser

    found = False
    while found != True:
        port = input("Input port used for connection: ")
        fullPort = "mongodb://localhost:" + str(port)
        if len(str(port)) != 5:
            print("Not a valid port number")
        else:
            found = True

    print(fullPort)
    client = pymongo.MongoClient(fullPort)
    db = client["291db"]

    collist = db.list_collection_names()
    Posts = db['Posts']
    Tags = db['Tags']
    Votes = db['Votes']
    #cursor Id
    #cursor_id = Posts.find().sort( "Id", -1 ).limit(1)
    cursor_id = Posts.find_one({"$query":{},"$orderby":{"_id":-1}})
    current_id = cursor_id["Id"]
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
    questions = None
    while loop != False:
        print("\n","Main Selection Menu")
        print("Type 'search question' to search for a question")
        print("Type 'post question' to post a question")
        if questions != None:
            print("Type 'list answers' to list all answers")
        print("Type 'quit' to exit program")
        menu = input()
        if menu.lower() == "search question":
            questions = search_for_questions()
        elif menu.lower() == "post question":
            post_a_question()
        elif menu.lower() == "list answers" and questions != None:
            list_answers(db,questions)
        elif menu.lower() == 'quit':
            sys.exit()


if __name__ == "__main__":
    main()
