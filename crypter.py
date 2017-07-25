from hashlib import blake2b

from Crypto.PublicKey import RSA

salt = b'7mwHBAFZBWM5Rc0g'
with open('public.pem', 'r') as f:
    public_key = RSA.importKey(f.read())


def word_hash(word):
    h = blake2b(salt=salt)
    h.update(word.encode('utf-8'))
    return h.hexdigest()


def word_encrypt(word):
    return public_key.encrypt(word.encode('utf-8'), 1)[0]


def word_decrypt(encrypted, key_data):
    private_key = RSA.importKey(key_data)
    return private_key.decrypt(encrypted)
