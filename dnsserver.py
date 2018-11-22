import socket
import threading
import numpy as np
import dns.name
import dns.query
import dns.dnssec
import dns.message
import dns.resolver
import dns.rdatatype


# Save
#dictionary = {'www.google.com':'10.4.1.4', 'www.facebook.com':'10.3.5.6'}
#np.save('dnsrecords.npy', dictionary) 

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

    if request in read_dnsentries.keys():
    	ip = read_dnsentries[request]
    else:
         ip = "Server IP could not be found"

    dnssec_validate(format_name(request))
    client_socket.send(ip)
    print('Sent {}'.format(ip))
    client_socket.close()

def dnssec_validate(domain_name):
    try:

        response = dns.resolver.query(domain_name, dns.rdatatype.NS)
        # look for the domain name in the nameserver
        # nameserver.send(domain_name)
        print(response.rrset)
        # get back the name of the nameserver containing this domain
        print(".............")
        nsname = response.rrset[0]
        print(nsname)
        print(".............")
        # get the IP of the nameserver
        response = dns.resolver.query(str(nsname), rdtype=dns.rdatatype.A)
        nsaddr = response.rrset[0].to_text()
        print(nsaddr)
        print(".............")
        # look for the DNS KEY for the domain name
        request = dns.message.make_query(domain_name, dns.rdatatype.DNSKEY, want_dnssec=True)
        print(request)
        print(".............")
        response = dns.query.udp(request, nsaddr)
        print("response :{}".format(response))
        print(".............")
        if response.rcode() != 0:
            print("SOMETHING WENT WRONG")
        answer = response.answer
        print(answer)
        print(".............")
        print(len(answer))
        if(len(answer)!=2):
            print("SOMETHING WENT WRONG")
        # print("answer:{}".format(answer[1]))
        name = dns.name.from_text(domain_name)
        # print("name:{}".format(name))
        try:
            # print("inside try....")
            dns.dnssec.validate(answer[0], answer[1], {name: answer[0]})
            print("DNSSEC Validated")
        except dns.dnssec.ValidationFailure as e:
            print("DNS Validation Failure : {}".format(e))

    except Exception as e:
        print(e)

def format_name(domain):
    name = domain[4:]
    name = name + '.'
    return name


while True:
    client_sock, address = server.accept()
    print('\n\nAccepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
