from Crypto import Random
from Crypto.PublicKey import RSA

# generate new key
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)

# export key to file
with open('private.pem', 'w') as f:
    f.write(key.exportKey('PEM').decode())
with open('public.pem', 'w') as f:
    f.write(key.publickey().exportKey('PEM').decode())
