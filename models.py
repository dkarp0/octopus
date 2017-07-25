from hashlib import blake2b

import sqlalchemy
from Crypto.PublicKey import RSA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, Session

Base = declarative_base()
salt = b'7mwHBAFZBWM5Rc0g'
with open('public.pem', 'r') as f:
    public_key = RSA.importKey(f.read())


class Words(Base):
    __tablename__ = 'words'
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    word = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    @validates('count')
    def validate_count(self, key, count) -> int:
        assert count > 0
        return count


def word_hash(word):
    h = blake2b(salt=salt)
    h.update(word.encode('utf-8'))
    return h.hexdigest()


def word_encrypt(word):
    return public_key.encrypt(word)


def word_decrypt(encrypted, key_data):
    private_key = RSA.importKey(key_data)
    return private_key.decrypt(encrypted)


def save(word_counts, s: Session):
    for w in word_counts:
        word = s.query(Words).filter_by(id=word_hash(w[0])).first()
        if word:
            word.update({'count': Words.count + w[1]})
        else:
            s.add(Words(id=word_hash(w[0]), word=word_encrypt(w[0]), count=w[1]))
    s.commit()


def get(s: Session, key):
    return [(word_decrypt(w.word, key), w.count) for w in s.query(Words).all()]
