import socket
import sys

import time
import datetime

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
counter = 1
now = datetime.datetime.now()

while True:
    # Wait for a connection
    print(sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stderr, 'connection from', client_address)
        #time.sleep(5)
        # Receive the data in small chunks and retransmit it
        now = datetime.datetime.now()

        while True:
            data = connection.recv(256)
            print (sys.stderr, 'received "%s"' % data)
            send_string = ''
            if data:
                if data == b'1':
                    send_string = 'OK'
                elif data == b'Date':
                    send_string = now.strftime("%d-%m-%Y %H:%M:%S")
                elif data == 'Count':
                    send_string = str(counter)
                else:
                    send_string = 'Something else'
                print(sys.stderr, 'sending data back to the client')
                connection.sendall(send_string.encode('utf8'))
            else:
                print (sys.stderr, 'no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
