import socket
import sys


class Client:

    def __init__(self,  server_address, port):
        super(self.__class__, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.server_address = (server_address, port)

    def connect(self):
        # Connect the socket to the port where the server is listening
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(sys.stderr, 'connecting to %s port %s' % self.server_address)
        self.sock.connect(self.server_address)
        self.connected = True

    def request(self, message):
        try:
            # Send data
            self.connect()
            self.sock.sendall(message.encode('utf8'))
            data = self.sock.recv(256)
            return data
        except OSError as e:
            self.connected = False
            return e

        finally:
            # print(sys.stderr, 'closing socket')
            self.sock.close()

