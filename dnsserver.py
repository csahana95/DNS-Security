import socket
import threading
import numpy as np
import dns.name
import dns.query
import dns.dnssec
import dns.message
import dns.resolver
import dns.rdatatype
from Crypto.Hash import SHA256

import dnssecserver

# Load
read_dnsentries = np.load('dnsrecords.npy').item()

# print(read_dnsentries)

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print('Received {}'.format(request))
    ip_addr = dnssecserver.query_addr(request)
    if ip_addr == 0:
        print("Server not found")
    else:
        print(ip_addr)
    if (dnssec_validate(request)):
        print("Signature verified")
        client_socket.send(ip_addr)
        print('Sent {}'.format(ip_addr))
    else:
        print("Signature validation failed")
        client_socket.send("Something went wrong")
    client_socket.close()


def dnssec_validate(domain_name):
    hash = SHA256.new(domain_name.encode('utf8')).digest()
    public_key = dnssecserver.query_DNSKEY()
    signature = dnssecserver.query_signature(domain_name)
    return public_key.verify(hash, signature)


while True:
    client_sock, address = server.accept()
    print('\n\nAccepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
