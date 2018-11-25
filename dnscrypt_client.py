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
import time
from pandas import DataFrame



def client_program():
	host = socket.gethostname()  # as both code is running on same pc
	port = 5000  # socket server port number

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server
	rec = np.load('dns_records.npy').item()
	query_no = list()
	resp_time = list()


	
	for i in range (1,901):
		servername = random.choice(rec.keys())
		rnd_gen = rnd.new().read
		client_key = RSA.generate(1024, rnd_gen)
		client_pub_key = client_key.publickey()
		t0= time.time()
		hash = SHA256.new(servername).digest()
		signature = client_key.sign(hash, '')


		#pri_key = key.privatekey()
		#key_to_send = key.exportKey()	
		#enc = pub_key.encrypt(servername,32)
		
		
		client_socket.send(pickle.dumps(client_pub_key))  # send message
		#print ("sent key: " +pub_key)
		data = client_socket.recv(1024)  # receive response
		server_key = pickle.loads(data)

		print('server key received')  # show in terminal
		client_socket.send(pickle.dumps(server_key.encrypt(servername,32))) #enc query by server public key
		client_socket.send(pickle.dumps(signature) )#client sign sent, instead of encrypting by client's private key
		

		
		ip_sign = pickle.loads(client_socket.recv(1024))
		data = pickle.loads(client_socket.recv(1024))
		print ("server response received")
		ip = client_key.decrypt((data))
		#print((ip))
		hash = SHA256.new(ip).digest()
		if server_key.verify(hash, ip_sign):
			print(" server hash verified")
		print(ip) 
		t1 = time.time()
		print("Time taken: {0}".format(t1-t0))
		query_no.append(i)
		resp_time.append(t1-t0)
		
	df = DataFrame({'Query Number': query_no, 'Response Time': resp_time})	
	df.to_excel('output.xlsx', sheet_name='sheet1', index=False)

		

	client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
