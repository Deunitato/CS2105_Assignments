import sys
from socket import *
import zlib

# There is no need for Bob to detect end of transmission and terminate. If you need to
# manually terminate it, press <Ctrl> + c.

#Algorithm planning






#Global variables are here and initialised
clientAddress = 0
serverPort = int(sys.argv[1]) #Get the arguments
bobSocket = socket(AF_INET,SOCK_DGRAM) #declare initialised UDP
#clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
bobSocket.bind(('localhost',serverPort))
expectedSeq = 0
packets = []


#Socket functions ============================

# #compress the packet
# def compressPacket(message):
#     return zlib.compress(message, level=-1)

# #deflate the packet as a string
# def deflatePacket(packet):
#     return zlib.decompress(packet)

def calculateCheckSum(received:str):
    checksum = zlib.crc32(received.encode())
    return checksum


#returns true if it is corrupted
def isCorrupted(received:str, mine:str):
    return not (received == calculateCheckSum(mine))


#Creates a Packet that is already encoded
#Requires Checksum, size of message, length, sequence number
#Packet header: seq  checksum  length   
#
# You are reminded again that each packet Alice or Bob sends should contain at most 64
# bytes of payload data (inclusive of user-defined header/trailer fields), or UnreliNET
# will drop it.
def makePacket(index:int):
    checksum = str(calculateCheckSum(str(index)))
    packet = checksum + " " +  str(index)
    return  packet.encode();


#returns the header and the message (Left over)
def getHeader(message):
    i =0
    message = message.decode()
    while(not message[i:i+3] == "   "):
        i = i +1
        if(i+3>len(message)):
            return False
    header = message [:i].split()
    if(len(header)< 3):
        return False
    
    checksum = header[0]
    calcChecksum = str(zlib.crc32(message[len(checksum) + 1:].encode()))
    if (checksum != calcChecksum):
        return False

    # try:
    #     tocheck = header[1]+ " "+ header[2] + " " + message[i+3:]
    #     if(checkPacket(header[0],int(header[1]),tocheck) and ( header[2]!= "Y" or header[2] !="N")):
    #         sendMessage(makePacket(expectedSeq))
    #         #print("Bad packet")
    #         return False
    # except ValueError:
    #     return False

    return header[0],header[1],header[2],message[i+3:]


#returns true if the packet is correct
#checks that message is uncorrupted
#checks that the sequence is the same as the next expected
#Assumptions: assume that message is the correct length already
def checkPacket(checksum, sequence:int, message):
    return (not isCorrupted(checksum, str(calculateCheckSum(message)))) and sequence <= expectedSeq




    
# Chat functions ===============================

#ensure the message is sent
def sendMessage(encodedMSG):
        #print("Attempt send at BOB" , encodedMSG.decode())
        bobSocket.sendto(encodedMSG,clientAddress)

#Bob Side of receiving
#Throws timeout error or invalid packet
def receiveMessage():
    #print("Attempt recieve at BOB")
    sentence = ""
    nextByte = "Y"
    global expectedSeq
    global clientAddress

    while(nextByte != "N"):
        
        modifiedMessage, clientAddress = bobSocket.recvfrom(64) #receive
        header = getHeader(modifiedMessage)
        if(not header):
            continue
        #print("Recieved exp", message) 
        try:
            checksum, EXPsequence, byte, message = header
            int(EXPsequence)
        except ValueError:
            continue


        if(int(EXPsequence) != expectedSeq): #check if recieve packet has been acked before
            sendMessage(makePacket(expectedSeq))
            #print("TResend ack")
            continue #move on to the next packet
        
        nextByte = byte
        expectedSeq = expectedSeq + 1
        sendMessage(makePacket(expectedSeq))
        sys.stdout.write(message)
        # sentence = sentence + message
        #print(message)
        #print("The message is: " , message)
        #print("The sentence is ", sentence)

    #print("Recieved successfull")





#MAIN PROGRAM HERE+===============================
receiveMessage()
# sys.stdout.write(sentence)

while True: #loop
    #waits for something
    modifiedMessage, clientAddress = bobSocket.recvfrom(64) #receive
    sendMessage(makePacket(expectedSeq+1))


