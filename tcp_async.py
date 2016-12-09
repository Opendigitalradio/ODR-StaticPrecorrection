"""Tcp client for asynchronous uhd message tcp port"""

import threading
import Queue
import time
import socket

class _TcpAsyncClient(threading.Thread):
    """Thead for message polling"""
    queue = Queue.Queue()
    q_quit = Queue.Queue()

    ip_address = None
    port = None
    BUFFER_SIZE = 1

    def __init__(self, ip_address, port):
        super(_TcpAsyncClient, self).__init__()
        self.ip_address = ip_address
        self.port = port

    def __exit__(self):
        self.stop()

    def run(self):
        """connect and poll messages to queue"""

        #Establish connection
        sock = None
        print("Connecting to asynchronous uhd message tcp port " + str(self.port))
        while self.q_quit.empty():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.ip_address, self.port))
                break
            except socket.error:
                print("connecting to asynchronous uhd message tcp port " + str(self.port))
                #traceback.print_exc()
                sock.close()
                time.sleep(0.5)
        print("Connected to asynchronous uhd message tcp port " + str(self.port))

        #Read messages
        sock.settimeout(1)
        while self.q_quit.empty():
            try:
                data = sock.recv(self.BUFFER_SIZE)
                self.queue.put(data)
            except socket.timeout:
                pass

        sock.close()

    def stop(self):
        """stop thread"""
        print("stop tcp_async uhd message tcp thread")
        self.q_quit.put("end")


class UhdAsyncMsg(object):
    """Creates a thread to connect to the asynchronous uhd messages tcp port"""

    def __init__(self, ip_address = "127.0.0.1", port = 47010):
        self.tcpa = _TcpAsyncClient(ip_address, port)
        self.tcpa.start()

    def __exit__(self):
        self.tcpa.stop()

    def stop(self):
        """stop tcp thread"""
        self.tcpa.stop()

    def get_res(self):
        """get received messages as string of integer"""
        out = ""
        while not self.tcpa.queue.empty():
            out += str(ord(self.tcpa.queue.get()))
        return out

    def has_msg(self):
        """Checks if one or more messages were received and empties the message queue"""
        return self.get_res() != ""
