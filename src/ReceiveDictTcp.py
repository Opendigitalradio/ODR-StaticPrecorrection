import socket
import threading
import json
from Queue import Queue
import sys

class ReceiveDictTcp(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.queue = Queue()
        self.thread = threading.Thread(target = self.listen)

    def start(self):
        self.thread.start()

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(0)
            print("connecting to " + str(client) + " " + str(address)) 
            self.listenToClient(client,address)

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    jresponse = data
                    response = json.loads(jresponse)
                    client.send(json.dumps(response))
                    self.queue.put(response)
                else:
                    raise Exception('disconnected')
            except Exception as e:
                print str(e)
                client.close()
                return False
