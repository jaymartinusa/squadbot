import praw
import re
from search import searchLayers

reddit = praw.Reddit('script1', user_agent='http://127.0.0.0')

subreddit = reddit.subreddit('SquadBot')

trigger = "?squadbot"

filename = "posts_replied_to.txt"

def ContainsCommand(comment):
    if trigger in comment:
        return True
    else:
        return False
    
def check(string):
    string = string.replace(trigger + " ", "")
    print(string)
    if re.match(r'"[\w -]*" "[\w -]*"', string):
        print("Both have quotes")
        newString = string.split("\" \"")
        i=0
        for string in newString:
            newString[i] = string.replace("\"", "")
            i+=1
        return newString
    elif re.match(r'[\w-]* "[\w ()-]*"', string):
        print("Only second has quotes")
        newString = string.split(" \"")
        i=0
        for string in newString:
            newString[i] = string.replace("\"", "")
            i+=1
        return newString
    elif re.match(r'"[\w -]*" \w*', string):
        print("Only first has quotes")
        newString = string.split("\" ")
        i=0
        for string in newString:
            newString[i] = string.replace("\"", "")
            i+=1
        return newString
    elif re.match(r'[\w-]* \w*', string):
        print("Neither have quotes")
        newString = string.split(" ")
        i=0
        for string in newString:
            newString[i] = string.replace("\"", "")
            i+=1
        return newString
    elif re.match(r'"[\w -]*"', string):
        print("Single command with quotes")
        newString = string.split("\" \"")
        i=0
        for string in newString:
            newString[i] = string.replace("\"", "")
            i+=1
        return newString
    elif re.match(r'[\w-]', string):
        print("Single word")
        newString = string.split("\" \"")
        i=0
        for string in newString:
            newString[i] = string.replace("\"", "")
            i+=1
        return newString
    else:
        return False


def GenerateResponse(comment):
    commands = [];
    splitComment = comment.split("\n")
    #print(splitComment)
    for line in splitComment:
        #print(line)
        if line.startswith(trigger):
            commands.append(line)
    for command in commands:
        response = check(command)
        if response:
            return response
    #return "The comment meets the criteria"
    return False

def NotYetRepliedTo(id):
    file = open(filename, "r")
    for line in file:
        if id in line:
            return False
    file = open(filename, "a")
    file.write(id+"\n")
    return True

for comment in subreddit.stream.comments():
    try:
        #print(10*'_' + str(comment.author) + 10*'_' + str(comment.permalink) + 10*'_')
        #print(comment.body)
        #print(3*'\n')
        print("--"+comment.id+"--")
        if NotYetRepliedTo(comment.id):
            if ContainsCommand(comment.body):
                print("True")
                response = GenerateResponse(comment.body)
                if response:
                    terms = response[0]
                    if len(response) > 1 and response[1]:
                        request = response[1]
                    else:
                        request = False
                    print("Terms: "+terms+" Request: "+str(request))
                    if request:
                        result = searchLayers(terms, [request], "reddit")
                        print(result)
                        comment.reply(result)
                    else:
                        result = searchLayers(terms, request, "reddit")
                        print(result)
                        comment.reply(result)
                    print(30*"_")
                        
                        
                #comment.reply(GenerateResponse(comment.body))
            else:
                print("False")   
    except praw.exceptions.PRAWException as e:
        pass


