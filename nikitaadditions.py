import pymongo
from pymongo import MongoClient
from datetime import date

# Use client = MongoClient('mongodb://localhost:27017') for specific ports!
# Connect to the default port on localhost for the mongodb server.



# Create or open the video_store database on server.



# List collection names.
user_id= ""
cursor_id = collist.find().sort( { "Id": -1 }).limit(1)

for post in cursor_id:
    current_id = post["Id"]

def search_for_questions():

    keyword_input = input("Type the keywords separated by comma and no spaces")
    keyword_list = keyword_input.split(",")

    search_result_array = []

    for keyword in keyword_list:
        results = collist.find({"$or":[
            {"PostTypeId": "1","Body": keyword },
            {"PostTypeId":"1", "Title": keyword},
            {"PostTypeId":"1", "Tags": keyword}

            ]})
        search_result_array = search_result_array + results

    counter = 1

    for result in search_result_array:
        print("Result: "+counter)
        print("Title: "+result["Title"])
        print("CreationDate: "+result["CreationDate"])
        print("Score: "+result["Score"])
        print("AnswerCount: "+result["AnswerCount"])

    input_post = input("Input the Result Number to select the post: ")
    correct_input = False

    while correct_input == False:
        try:
            input_post = int(input_post)
            
            if input_post > 0 and input_post <= len(search_result_array)+1:
                collist.update_one({"ViewCount": , "$inc":"ViewCount": 1})
                correct_input = True
                action_answer_input= input("Do you want to answer this question? [y for yes and anything else for no]")
                if action_answer_input == "y":
                    question_action_answer(search_result_array[input_post-1]["Id"])

                return search_result_array[input_post-1]["Id"]
        
            else:
                print("Post does not exist, try again")
                input_post = input("Input the Result Number to select the post: ")


        except: 
            print("Wrong Input")
            input_post = input("Input the Result Number to select the post: ")


def post_a_question()

    input_title= input("Title text:")
    input_body_text = input("Body text:")
    input_tags = input("Add zero or more tags in this format - <hardware><mac><powerpc><macos>")



    new_post = { 
    "Id": string(int(current_id)+1),
    "PostTypeId": "1",
    "CreationDate": date.today(),
    "Score": 0,
    "ViewCount": 0,
    "Body": input_body_text,
    "OwnerUserId": user_id,
    "Title": input_title,
    "Tags": input_tags,
    "AnswerCount": 0,
    "CommentCount": 0,
    "ContentLicense": "CC BY-SA 2.5" 

    }
    current_id = string(int(current_id)+1)

    collist.insert_one(new_post)



def question_action_answer(question_id)

    
    input_body_text = input("Body text:")
    



    new_post = { 
    "Id": string(int(current_id)+1),
    "PostTypeId": "2",
    "ParentId": question_id
    "CreationDate": date.today(),
    "Score": 0,
    "ViewCount": 0,
    "Body": input_body_text,
    "OwnerUserId": user_id,
    "AnswerCount": 0,
    "CommentCount": 0,
    "ContentLicense": "CC BY-SA 2.5" 

    }

    current_id = string(int(current_id)+1)

    collist.insert_one(new_post)











    
