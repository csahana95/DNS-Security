import socket
import sys
import time
import hashlib as hlb
import numpy as np
import random
from Crypto.PublicKey import RSA
from Crypto import Random as rnd
from Crypto.Util import randpool
import pickle
from Crypto.Hash import SHA256


def server_program():
    read_dnsentries = np.load('dns_records.npy').item()
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
	
    while True:
	 rnd_gen = rnd.new().read
	 server_key = RSA.generate(1024, rnd_gen)
	 server_pub_key = server_key.publickey()
	 data = conn.recv(1024)
	 client_key = pickle.loads(data)
	 print("client key recieved ")

      
	 conn.send(pickle.dumps(server_pub_key))  # send data to the client
	 msg = pickle.loads(conn.recv(1024))
	 query_sign = pickle.loads(conn.recv(1024))
	 #dec = rec_key.decrypt(msg)
	 query = server_key.decrypt((msg))
	 print ("query received")
	 #print(type(query))
	 
	 if client_key.verify(SHA256.new(query).digest(), query_sign):
		print(" Client hash verified")
	 
		
	 if query in read_dnsentries.keys(): # and request[1] == hlb.sha512(request[0]).hexdigest() :
		ip = read_dnsentries[query]
	 enc_ip = client_key.encrypt(ip,32) #encrypt response by client public key
	 hash = SHA256.new(ip).digest()
	 #print((ip))
	 signature = server_key.sign(hash, '')
	 conn.send(pickle.dumps(signature))
	 conn.send(pickle.dumps(enc_ip))

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
