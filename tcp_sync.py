"""Tcp client for synchronous uhd message tcp port"""

import threading
import Queue
import time
import socket
import struct

class _TcpSyncClient(threading.Thread):
    """Thead for message polling"""
    queue = Queue.Queue()
    q_quit = Queue.Queue()

    ip_address = None
    port = None

    def __init__(self, ip_address, port):
        super(_TcpSyncClient, self).__init__()
        self.ip_address = ip_address
        self.port = port

    def __exit__(self):
        self.stop()

    def run(self):
        """connect and poll messages to queue"""

        #Establish connection
        sock = None
        print("Connecting to synchronous uhd message tcp port " + str(self.port))
        while 1:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.ip_address, self.port))
                break
            except socket.error:
                print("connecting to synchronous uhd message tcp port " + str(self.port))
                #traceback.print_exc()
                sock.close()
                time.sleep(0.5)
        print("Connected to synchronous uhd message tcp port " + str(self.port))

        #Read messages
        sock.settimeout(None)
        while self.q_quit.empty():
            try:
                s = sock.recv(12)
                res_tuple = struct.unpack(
                        "fff",
                        s)
                assert(type(res_tuple) is tuple), (type(res_list), res_tuple)
                self.queue.put(res_tuple)
            except socket.timeout:
                traceback.print_exc()
                pass

        sock.close()

    def stop(self):
        """stop thread"""
        print("stop tcp_sync uhd message tcp thread")
        self.q_quit.put("end")


class UhdSyncMsg(object):
    """Creates a thread to connect to the synchronous uhd messages tcp port"""

    def __init__(self, ip_address = "127.0.0.1", port = 47009):
        self.tcpa = _TcpSyncClient(ip_address, port)
        self.tcpa.start()

    def __exit__(self):
        self.tcpa.stop()

    def stop(self):
        """stop tcp thread"""
        self.tcpa.stop()

    def get_res(self):
        """get received messages as string of integer"""
        out = []
        while not self.tcpa.queue.empty():
            out.append(self.tcpa.queue.get())
        return out

    def has_msg(self):
        """Checks if one or more messages were received and empties the message queue"""
        return self.get_res() != ""
