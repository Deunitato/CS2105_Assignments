
import sys
import zlib

filename = sys.argv[1] 
buffer = open(filename, 'rb').read()
checksum = zlib . crc32 ( buffer )
print checksum & 0xffffffff
