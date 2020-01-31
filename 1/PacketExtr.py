import sys
# read **at most ** 5 bytes from stdin
headerfile = sys.stdin.buffer.read(6)# take size


while len(headerfile) == 6:
    data = sys.stdin.buffer.read(1)
    number = b''
    # number += data
    while data != b'B': # get the number
          number += data
          data = sys.stdin.buffer.read(1)
          
    payLoad = sys.stdin.buffer.read(eval(number))
# write data to stdout and flush immediately
    sys.stdout.buffer.write(payLoad)
    sys.stdout.buffer.flush()
    headerfile = sys.stdin.buffer.read(6)# take size
