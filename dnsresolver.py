from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import dnsserver
# from Crypto import Signature

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)

public_key = key.publickey()
text = 'sdfhifvn'
hash = SHA256.new(text.encode('utf8')).digest()
signature = key.sign(hash, '')


print(signature)
print(public_key.verify(hash, signature))
