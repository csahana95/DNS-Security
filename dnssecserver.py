from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import numpy as np

# Load
read_dnsentries = np.load('dnsrecords.npy').item()

# Generate key
random_generator = Random.new().read
__key = RSA.generate(1024, random_generator)
DNS_KEY = __key.publickey()
RRSIG = {}
# from Crypto import Signature
for each in read_dnsentries.keys():
    domain = each
    hash = SHA256.new(domain.encode('utf8')).digest()
    signature = __key.sign(hash, '')
    RRSIG[each] = signature

def query_addr(domain):
    if domain in read_dnsentries.keys():
        return read_dnsentries[domain]
    else:
        return 0

def query_DNSKEY():
    DNS_KEY = __key.publickey()
    return DNS_KEY

def query_signature(domain):
    return RRSIG[domain]

