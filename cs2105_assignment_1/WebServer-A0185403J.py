import socket
import sys

#GLOBAL VARIABLES
Dict = {} 
Header = {}




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

#sets the connection of TCP, returns the socket if is established
def setConnection(portNum):
    #creates socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('',int(portNum))
    # print("starting up on" , server_address, "on port" , portNum)#for debugging
    soc.bind(server_address)

    return soc

#checks if the headerpair is correct for first substring
def isValidMethod(pair1, pair2):
    if(pair1=="post" or pair1 == "get" or pair1=="delete" or pair1==" post" or pair1 == " get" or pair1==" delete"): #compulsory substring
        if("/key/" in pair2):
            return True
        else:
            return False
    else:
        return False

def isValidPost(pair1):
    if(pair1 == "content-length" or pair1 == " content-length"):
        return True
    else:
        return False

def InitHeader():
    Header = {
    "Method" ,
    "Key",
    "Length", #optional
    }


#gets user input
portNum = sys.argv[1] 

socket = setConnection(portNum)
# Listen for incoming connections
socket.listen(1)
#get connections
connection, client_address = socket.accept()


#get first sentence

sentence = connection.recv(1024)
#sentence = b''
#init header
InitHeader()

while True:
    n=0
    #get header

    # print("sentence at the start:"+ sentence.decode())
    

    
    #gets the header===========================================================================
    front = ""
    while(sentence[n] != 32 or sentence[n+1] != 32):
        n = n+1;
        if(n+1 == len(sentence)):
            sentence = sentence + connection.recv(1024) #recover more in case it comes in 2 batches
    front = (sentence[0:n]).decode() #decode it
    sentence = sentence[n+2:] #skip


    #get Key and method ========================================================================
    index = 0
    getHeader = front.split(" ")
    while(True):
        pair1 = getHeader[index].lower()
        pair2 = getHeader[index +1]
        # print("header", pair1)
        # print("key", pair1)
        if(isValidMethod(pair1,pair2)):
            keyPrefix = "/key/"
            key = pair2.partition(keyPrefix)[2] #gets the key after prefix
            Header["Key"] = key #needget the /key/
            Header["Method"] = pair1
            break;
        else:
            index = index + 2 #skip to next pair
    

    # print("The sentence after get method:" +sentence.decode())
    # print("with size", str(len(sentence.decode())))

    #post method if can =================================================================================
    if(Header["Method"] == "post"):
        index = 0
        getHeader = front.split(" ")
        while(True):
            pair1 = getHeader[index].lower()
            # print("p1", pair1)
            
            pair2 = getHeader[index + 1]
            # print("p2", pair2)
            # print("with size:", len(pair2))
            if(isValidPost(pair1)):
                Header["Length"] = int(pair2)
                break;
            else:
                index = index + 2 #skip to next pair
    # print("The method:" + Header["Method"])
    # print("The key:" + Header["Key"])
    # print("The length:" + str(Header["Length"]))
    # print("Length of left over ", len(sentence))
    n=0

    #checking
    method = Header["Method"]
    key = Header["Key"]
    lengthOfMessage = Header["Length"]
    # print("The method: " + method)
    # print("The key: " + key)

    #serve the port from here on====================================================================

    #get
    if(method == "get"):
        # print("get is called")
        returnData = callGet(key)
        #sentence = sentence[n+2:]

    #post
    elif(method == "post"):
        message = b''
        # print("The sentence:" +sentence.decode())
        while (len(sentence) < lengthOfMessage): #not enough..
            sentence = sentence + connection.recv(1024)
        message = sentence[:lengthOfMessage] #getmy message
        
        sentence = sentence[lengthOfMessage:] #move my pointer
        # print("The sentence after:" +sentence.decode() + ",with the size of ", len(sentence))
        # print("The messages:" +message.decode() + ",with the size of ", len(message))
        returnData = callPost(key,message) #submit post

    #delete
    elif(method == "delete"):
        returnData = callDel(key)
        #sentence = sentence[n+2:]
    else: 
        # print("wrong comman FIAKED")
        returnData = "404 NotFound".encode()
        #sentence = sentence[n+2:]

    # Clean up the connection
    # print("THis is the leftover sentence:" , sentence.decode())
    InitHeader()
    connection.send(returnData)
    if(len(sentence)==0): #will close socket if timeout error
        sentence = connection.recv(1024)
        # print("THis is the inside" , sentence.decode())
        if(len(sentence)==0):
            connection.close()
            # print("connection close suc")
            connection, client_address = socket.accept()
            # print("connection openned suc")
            sentence = connection.recv(1024)
            