# DNS-Security
Comparison of DNS, DNS Sec and DNS crypt

Usage:
>>python dnsserver.py<br/>
python dnsclient.py www.google.com


# DNS_SEC
python dnsserver.py<br/>
python dnssecclient.py


1. dnsserver receives request from client and asks dnssecserver to provide the ip address
2. it also verifies the signature of the domain name to make sure information is not altered on the way


