import socket
from utils import build_response

PORT = 53
IP = "127.0.0.1"

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((IP, PORT))

while True:
    try:
        data, addr = soc.recvfrom(512)
        result = build_response(data)
        soc.sendto(result, addr)
    except:
        print("Data not available")
