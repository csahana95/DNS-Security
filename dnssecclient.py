import socket
import time
import numpy as np
import random
from pandas import DataFrame

rec = np.load('dnsrecords.npy').item()
query_no = list()
resp_time = list()

for itr in range(900):
    servername = random.choice(rec.keys())
    # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    # client.connect((target, port))
    t0 = time.time()
    client.connect(('0.0.0.0', 9999))
    print t0
    # send some data (in this case a HTTP GET request)
    client.send(servername)
    # receive the response data (4096 is recommended buffer size)
    response = client.recv(4096)
    t1 = time.time()
    query_no.append(itr)
    resp_time.append((t1-t0)*100)
    print(response)
    print("Time taken: {0}".format(t1 - t0))

df = DataFrame({'Query Number': query_no, 'Response Time': resp_time})
df.to_excel('output.xlsx', sheet_name='sheet1', index=False)

client.close()