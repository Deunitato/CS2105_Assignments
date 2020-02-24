import socket
import sys

Dict = {} 
#1. Insertion and update
#(a) The HTTP request method should be POST and the value to be inserted (or
#updated) constitutes the content body. There should also be a Content
#Length header indicating the number of bytes in the content body.
#(b) The server should respond with a 200 OK status code after inserting or up
#dating the value. The client always expects success statuses for insertions
#and updates.
def callPost(key, value):
    Dict[key] = value
    return "200 OK  ".encode()

#2. Retrieval
#(a) The HTTP request method should be GET, and there is no content body.
#(b) If the key does not exist in the key-value store, the server returns a 404
#NotFound status code. Otherwise, the server should return a 200 OK code,
#the correct Content-Length header and the value data in the content body.
def callGet(key):
    if(key in Dict):
        contentBody = Dict[key]
        contentLength = "content-length " + str(len(contentBody))
        encodedmesg = "200 OK " + contentLength +"  "
        return encodedmesg.encode() + contentBody
    else:
        return "404 NotFound  ".encode()

#3. Deletion
#(a) The HTTP request method is DELETE, and there is no content body.
#(b) If the key does not exist, the server returns a 404 NotFound code. Otherwise,
#it should delete the key-value pair from the store and respond with a 200 OK
#code and the deleted value string as the content body. The Content-Length
#header should also be sent accordingly.
def callDel(key):
    if(key in Dict):
        contentBody = Dict.pop(key,None)
        contentLength = "content-length " + str(len(contentBody))
        encodedmesg = "200 OK " + contentLength +"  " 
        return encodedmesg.encode() + contentBody
    else:
        return "404 NotFound  ".encode()


#gets user input
portNum = sys.argv[1] 

#creates socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('',int(portNum))
print("starting up on" , server_address, "on port" , portNum)#for debugging
soc.bind(server_address)

# Listen for incoming connections
soc.listen(1)
connection, client_address = soc.accept()
sentence = connection.recv(1024)


while True:
    # Wait for a connection
    
    n=0
    front = ""
    while(sentence[n] != 32 or sentence[n+1] != 32 ): #gets the decodable part
        n = n+1;
        if(n == len(sentence)):
            sentence = sentence + connection.recv(1024) #recover more in case it comes in 2 batches
    front = (sentence[0:n]).decode() #decode it

    print("front:",front)
    data = front.split(" ") # 0 = httptype, 1= key, 2 = optional content header , 3 = numberofChar, 4 = message
    method = (data[0]).lower() #ensure case insensitivity
    keyPrefix = "/key/"
    key = data[1].partition(keyPrefix)[2] #gets the key after prefix
    print("The method: " + method)
    print("key :", key)

    #get rid of dummies here
    if(method == "post"):
        count = 2
        while(count<len(data)):
            if((data[count]).lower() == "content-length"):
                lengthOfMessage = int(data[count + 1])
                break
            count = count +2 #skips pairs
    print("The length: " + str(lengthOfMessage))

    #serve the port
    if(method == "get"):
        returnData = callGet(key)
        sentence = sentence[n+2:]
    elif(method =="post"):
        nextmsg = b''
        sentenceMax = len(sentence)
        if(sentenceMax - (n+2) > lengthOfMessage): #if it overshots
            message = (sentence[n+2:n + 2  +lengthOfMessage])
            sentence = sentence[n+2 +lengthOfMessage:] #incase the nextmsg stole the part of the header
        else: #it does not overshot
            message = (sentence[n+2:])
            sentence = b''
        while True:
            if(len(message) < lengthOfMessage):
                nextmsg =  connection.recv(1024)
                sentenceMax = len(nextmsg)
                lenOfcurrent = len(message)
                if(sentenceMax - (n+2) > lengthOfMessage): #if it overshots
                    message = message + (nextmsg[lenOfcurrent:lenOfcurrent +lengthOfMessage])
                    missingHeader = lenOfcurrent +lengthOfMessage
                    sentence = nextmsg[missingHeader:] #incase the nextmsg stole the part of the header
                else: #it does not overshot
                    message = message + (nextmsg[lenOfcurrent:])
                    sentence = b''
            else:
                break
            message = message + nextmsg #append the message
        returnData = callPost(key,message) #submit post
    elif(method == "delete"):
        returnData = callDel(key)
        sentence = sentence[n+2:]
    else: 
        print("wrong comman FIAKED")
        returnData = "404 NotFound".encode()
        sentence = sentence[n+2:]

    # Clean up the connection
    print("THis is the leftover sentence" , sentence.decode())
    connection.send(returnData)
    if(len(sentence)==0): #will close socket if timeout error
        check = connection.recv(1024) #check again
        if(len(check) == 0):
            connection.close()
            print("connection close suc")
            soc.listen(1)
            connection, client_address = soc.accept()
            print("connection openned suc")
            sentence = connection.recv(1024)
        else:
            print("check is " , check.decode())
            sentence = check