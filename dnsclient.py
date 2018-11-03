import socket
import sys
#hostname, sld, tld, port = 'www', 'integralist', 'co.uk', 80
#target = '{}.{}.{}'.format(hostname, sld, tld)
servername = sys.argv[1]
# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('0.0.0.0', 9999))

# send some data (in this case a HTTP GET request)
client.send(servername)

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

print response