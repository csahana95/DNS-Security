import random
import string
import numpy as np

records = {}
for i in range(1000):  # number of urls you wanna generate
    rand = ''.join([random.choice(string.ascii_letters)
                    for n in range(14)])  # urls of length 14
    a = str(random.randint(1, 256))
    b = str(random.randint(1, 256))
    c = str(random.randint(1, 256))
    d = str(random.randint(1, 256))
    ip = a + '.' + b + '.' + c + '.' + d
    records[rand] = ip

    np.save('dnsrecords.npy', records)