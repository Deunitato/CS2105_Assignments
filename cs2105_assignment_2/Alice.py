import sys
from socket import *
import zlib

# Alice should terminate once all input
# is read from user and properly forwarded (i.e. the input stream is closed and everything
# in the input stream is successfully received by Bob)



#Algorithm planning

# - Sending
# 1.  create header - src, dest length, CheckSum
# - Sequence number shld be expected from bob
# 2. Attach to packet
# 3. Send to server
# 4 wait for recieve ack (Confirmation) - > Timeout : Resend, wrong packet: Resend

# - Receiving
# 1. Decipher
# 2. Check

# 3a. Extract  - > 4
# 3b. Resend sequence number of expected if wrong checksum -> 1
#
# 4. Read and print
#5 Go to sending if have






#Global variables are here and initialised
serverName = 'localhost'
serverPort = int(sys.argv[1]) #Get the arguments
clientSocket = socket(AF_INET,SOCK_DGRAM) #declare initialised UDP
#clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#clientSocket.bind(('',int(serverPort))) 
clientSocket.settimeout(0.1)
mySequence = 0
WINDOW_SIZE = 3
maxSequence = 0
packets = []


#Socket functions ============================


#calculate the byte size of the string
#this is to split the message if it exceeds 64
# Returns an integer of string
def calByte(myString:str):
    #mybytes = sys.getsizeof(myString)
    mybytes = len(myString.encode())
    #print("[calByte]String:" + myString + "," ,mybytes) #test functions
    return mybytes

# #checks that the given message is less than 64
# #returns true if the bytes are lesser than 64
def checkBytes(message:str):
    mbytes = calByte(message)
    return mbytes<40 #set it as 45 to make space for header

#compress the packet
# def compressPacket(message):
#     calByte(message) #remove this rmb ================================================= test
#     return zlib.compress(message, level=-1)

# #deflate the packet as a string
# def deflatePacket(packet):
#     return zlib.decompress(packet)

def calculateCheckSum(received:str):
    checksum = zlib.crc32(received.encode())
    return checksum


#returns true if it is corrupted
def isCorrupted(received:str, mine:str):
    return not (received == mine)


#Creates a Packet that is already encoded
#Requires Checksum, size of message, length, sequence number
#Packet header: seq  checksum  length   
#
# You are reminded again that each packet Alice or Bob sends should contain at most 64
# bytes of payload data (inclusive of user-defined header/trailer fields), or UnreliNET
# will drop it.
def makePacket(message, hasNext, index):
    sequence = str(index)
    tocheck = sequence + " " + hasNext + "   "+ message
    checksum = str(calculateCheckSum(tocheck))
    packet = checksum + " " + tocheck
    return  packet.encode();


#returns the checksum and the ack seq
def getHeader(message):

    header = message.decode().split()
    if(len(header)< 2):
        return False
    return header[0],header[1]

#returns true if the packet is correct
#checks that message is uncorrupted
#checks that the sequence is the same as the next expected
#Assumptions: assume that message is the correct length already
def checkPacket(checksum:str, sequence:int):
    return checksum == str(calculateCheckSum(str(sequence)))


#Filles the buffer if the message is too long
def fillBuffer(message):
    buffer = message
    global maxSequence
    index = 0
    while(True): #while it is larger than 64
        if(checkBytes(buffer)):#lets say it is within range 64
            #print("\nEnded fill buffer\n")
            packets.append(makePacket(buffer, "N",index)) #make a packet that does not have next trailing
            #print("Buffer:", buffer)
            index = index + 1
            break;
        #print("\making packet ", index)
        encodedMSG = makePacket(buffer[:45],"Y",index)
        buffer = buffer[45:] #get the rest
        packets.append(encodedMSG) #store the packet according to sequence
        index = index + 1

    maxSequence = index



    
# Chat functions ===============================

#sends everything within the window starting with the index given
def sendMessage(startIndex:int):
        global maxSequence
        #print("Attempt send at ALICES")
        index = startIndex
        while(index != maxSequence and index <= (startIndex + WINDOW_SIZE)):
            clientSocket.sendto(packets[index],(serverName, serverPort))
            index = index + 1

#returns uncorrupted msg
#throws exception if corrupted or timeout
#do busy waiting here.. wait for confirmation
def receiveMessage():
    sentence = ""

    global mySequence
    global maxSequence
    # print("waiting is ", waiting)
    # print("max: ", maxSequence)
    # print("entered while loop with waiting: ", WINDOW_SIZE)
        # print("entered while loop with waiting: ", waiting)
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(64)
        #print("I got an recieve,",modifiedMessage)
    except timeout:
        return False

    header = getHeader(modifiedMessage) #get the checksum and sequence
    if(not header):
        return False
    try:
        checksum,EXPsequence = header
        EXPsequence = int(EXPsequence)
    except ValueError:
        return False

    if(checkPacket(checksum, EXPsequence)):
        #print("checkpack")
        if EXPsequence > mySequence:
            mySequence = int(EXPsequence) #save the next expected
            print("mysequence:",mySequence)
    #clientSocket.sendto(packets[EXPsequence],(serverName, serverPort))
    return True






#MAIN PROGRAM HERE+===============================
message = ""
for line in sys.stdin:
    message = message + line


#encodedMSG = compressPacket(makePacket(message)) #encode before compressing
#packets[mySequence] = encodedMSG #store the packet according to sequence
fillBuffer(message) #fill buffer
mySequence = 0  #incrememnt my next sequence
while True: #loop

    #will contu send the nessage until 

        sendMessage(mySequence)
        receiveMessage() #will try to recieve the message the size of window

        if(mySequence > maxSequence):
            break


clientSocket.close()

