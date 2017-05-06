import time
import socket
import json

class SendDictTcp(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                self.buffer_size = 1024
                break
            except:
                print("Waiting for connecetion to %s:%d" %(self.host, self.port))
                time.sleep(1)

    def send(self, msg):
        self.sock.send(json.dumps(msg))
        return self.sock.recv(self.buffer_size)
