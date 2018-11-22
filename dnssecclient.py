import socket
import time
import numpy as np
import random

rec = np.load('dnsrecords.npy').item()

for itr in range(100):
    servername = random.choice(rec.keys())
    # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    # client.connect((target, port))
    client.connect(('0.0.0.0', 9999))
    t0 = time.time()
    # send some data (in this case a HTTP GET request)
    client.send(servername)

    # receive the response data (4096 is recommended buffer size)
    response = client.recv(4096)
    t1 = time.time()

    print(response)
    print("Time taken: {0}".format(t1 - t0))
