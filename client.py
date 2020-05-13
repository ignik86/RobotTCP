import socket
import sys
import time

message = 'Plan'
while True:

    #if message == b'OK':
      #  message = '2'
    #else:
     #   message = '1'
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.24.14.211', 1025)
    print (sys.stderr, 'connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:

        # Send data

        print (sys.stderr, 'sending "%s"' % message)

        sock.sendall(message.encode('utf8'))

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(32)
            amount_received += len(data)
            print(sys.stderr, 'received "%s"' % data)
            #message = data
    finally:
        print (sys.stderr, 'closing socket')
        sock.close()
    time.sleep(5)
