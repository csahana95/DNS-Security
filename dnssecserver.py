from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

# from Crypto import Signature

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)

DNS_KEY = key.publickey()

text = 'sdfhifvn'
hash = SHA256.new(text.encode('utf8')).digest()
signature = key.sign(hash, '')
RRSIG = signature
print(signature)
print(DNS_KEY.verify(hash, signature))
