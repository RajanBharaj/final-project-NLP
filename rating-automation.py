# Import Module
import os
  
# Folder Paths - to run on your computer, update to relevant file paths
binary_path = "drive:\\user\\location\\aclImdb\\binary_classification\\"
train_path = "drive:\\user\\location\\aclImdb\\train\\"
test_path = "drive:\\user\\location\\aclImdb\\test\\"

#classes
class Review:
    user_rating = 0 #rating given by user
    description = "" #text body of user review
    objective = False #review objectivity
    sentiment_rating = 0 #rating given by program
    sentiment = "" #"positive"/"negative"/"mixed"
    sentiment_evidence = []
    rating_disparity = 0 #percentage disparity
    reliable = False #reliability test

#global variables
max_rating = 10
#review sets

movie_reviews = []
disparity_accumulator = 0
reliability_accumulator = 0
total_disparity = 100
total_reliability = 0

# Read text File 
def read_text_file(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        return f.read()
    
# iterate through all folders/files in directory
for folder in os.listdir(train_path):
    # create folder path
    folder_path = train_path + "\\" + folder
    # check folder
    if os.path.isdir(folder_path):
        if folder == "neg":
            print("add negative reviews: start")
            # iterate through files in folder
            for file in os.listdir(folder_path):
                # Check whether file is in text format or not
                if file.endswith(".txt"):
                    file_path = f"{folder_path}\{file}"
                    # create review object
                    this_review = Review()
                    # get user given rating from file name
                    if int(file[-5]) == 0:
                        this_review.user_rating = 10
                    else:
                        this_review.user_rating = int(file[-5])
                    # call read text file function and add review to object
                    this_review.description = read_text_file(file_path)
                    # add review to list of reviews
                    movie_reviews.append(this_review)
            print("add negative reviews: complete\n")
        elif folder == "pos":
            print("add positive reviews: start")
            # iterate through files in folder
            for file in os.listdir(folder_path):
                # Check whether file is in text format or not
                if file.endswith(".txt"):
                    file_path = f"{folder_path}\{file}"
                    # create review object
                    this_review = Review()
                    # get user given rating from file name
                    if int(file[-5]) == 0:
                        this_review.user_rating = 10
                    else:
                        this_review.user_rating = int(file[-5])
                    # call read text file function and add review to object
                    this_review.description = read_text_file(file_path)
                    # add review to list of reviews
                    movie_reviews.append(this_review)
            print("add positive reviews: complete\n")
        else:
            print("list of movie reviews complete\n")

#primary functions
def analyse_sentiment(r):
    # example not algo
    if r.user_rating > 5:
        r.sentiment = "positive"
    elif r.user_rating < 5:
        r.sentiment = "negative"

def calculate_disparity(r): #complete
    disparity = r.user_rating - r.sentiment_rating
    if disparity < 0:
        disparity *= -1
    r.rating_disparity = (disparity/max_rating) * 100 #percentage disparity

def test_reliability(r): #complete
    test_rating = ""
    test_evidence = ""

    if r.sentiment == "positive":
        if 6 <= r.sentiment_rating <= 10:
            test_rating = "pass"
        else:
            test_rating = "fail"
    elif r.sentiment == "negative":
        if 1 <= r.sentiment_rating <= 4:
            test_rating = "pass"
        else:
            test_rating = "fail"
    elif r.sentiment == "mixed":
        if 3 <= r.sentiment_rating <= 7:
            test_rating = "pass"
        else:
            test_rating = "fail"
    else:
        print("review sentiment tagged incorrectly")

    tally_evidence = 0
    for e in r.sentiment_evidence:  
        if e[1] == "p":
            tally_evidence += 1
        elif e[1] == "n":
            tally_evidence -= 1
        else:
            print("sentiment evidence tagged incorrectly")
    if tally_evidence <= 0:
        if r.sentiment == "positive":
            test_evidence = "fail"
        else:
            test_evidence = "pass"
    elif test_evidence >= 0:
        if r.sentiment == "negative":
            test_evidence = "fail"
        else:
            test_evidence = "pass"

    if test_rating == "pass" and test_evidence == "pass":
        r.reliable = True
    else:
        r.reliable = False
    
#program
print("analyses: start")
for r in movie_reviews:
    analyse_sentiment(r)
    calculate_disparity(r)
    disparity_accumulator += r.rating_disparity
    test_reliability(r)
    if r.reliable == True:
        reliability_accumulator +=1
    #print(str(r.__dict__), "\n")

total_disparity = disparity_accumulator / len(movie_reviews)
total_accuracy = 100 - total_disparity
total_reliability = (reliability_accumulator / len(movie_reviews)) * 100

print("analyses: completed.\n")

#output
print("Total reviews: ", len(movie_reviews))
print("Rating disparity [mean avg.]: ", total_disparity, "%")
print("Rating accuracy [mean avg.]: ", total_accuracy, "%")
print("Reliability: ", total_reliability, "%")