# DNS-Security
Comparison of DNS, DNS Sec and DNS crypt

Usage:
>>python dnsserver.py<br/>
python dnsclient.py www.google.com

# DNScrypt
Use python 2.x.x to test.
The client will randomly choose domain names from dns_records file and perform query according to DNScrypt protocol.
To stop at any time, hit ctrl+C.

PS: Strictly speaking, DNScrypt uses elliptic curve cryptography but for the sake of simplicity we have used RSA. Also, say at client's end, the query should have been encrypted using server's public key and client's private key. But instead, we encrypted it only using 
server's public key and to compensate for encryption by client's private key and intital certificate exchange, we exchanged the hash-ed signatures. This so holds for server's end as well.
