import socket
import json

class SendDictTcp(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.buffer_size = 1024

    def send(self, msg):
        self.sock.send(json.dumps(msg))
        return self.sock.recv(self.buffer_size)
