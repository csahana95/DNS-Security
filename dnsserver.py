import socket
import threading
import numpy as np

# Save
#dictionary = {'www.google.com':'10.4.1.4', 'www.facebook.com':'10.3.5.6'}
#np.save('dnsrecords.npy', dictionary) 

# Load
read_dnsentries = np.load('dnsrecords.npy').item()

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print 'Received {}'.format(request)
    if request in read_dnsentries.keys():
    	ip = read_dnsentries[request]
    else:
         ip = "Server IP could not be found"

    client_socket.send(ip)
    print 'Sent {}'.format(ip)
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print '\n\nAccepted connection from {}:{}'.format(address[0], address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
