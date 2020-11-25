import pymongo, os
from datetime import date
from pymongo import MongoClient

currentUser = ''
cursor_id = None


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
    #Probably not meant to be ID
    cursor_id = Posts.find().sort( "Id", -1 ).limit(1)
    for post in cursor_id:
        current_id = post["Id"]
        print(current_id)
    #User ID get here
    #ID is optional
    u = input("Enter user ID or type skip: ")
    if u.lower() == "skip":
        currentUser = ''
    else:
        currentUser = u
    
    if currentUser != '':
        print(currentUser)
        returns = Posts.find({"OwnerUserId":currentUser})
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
    search_postID = search_for_questions()
    list_answers(db,search_postID)
    
    
if __name__ == "__main__":
    main()