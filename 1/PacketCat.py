import sys

header_sub = sys.stdin.buffer.read(6)

while len(header_sub) == 6:
    size_in_bytes = b''
    byte = sys.stdin.buffer.read(1)
    while byte != b'B':
        size_in_bytes += byte
        byte = sys.stdin.buffer.read(1)

    packet_size = eval(size_in_bytes)
    payload = sys.stdin.buffer.read(packet_size)
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()

    header_sub = sys.stdin.buffer.read1(6)
