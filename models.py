import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, Session

import crypter

Base = declarative_base()


class Words(Base):
    __tablename__ = 'words'
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True, nullable=False)
    word = sqlalchemy.Column(sqlalchemy.Binary(), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    @validates('count')
    def validate_count(self, key, count) -> int:
        assert count > 0
        return count


def save(word_counts, s: Session):
    for w in word_counts:
        word = s.query(Words).filter_by(id=crypter.word_hash(w[0])).first()
        if word:
            word.count = word.count + w[1]
            s.add(word)
        else:
            s.add(Words(id=crypter.word_hash(w[0]), word=crypter.word_encrypt(w[0]), count=w[1]))
    s.commit()


def get(s: Session, key):
    return [(crypter.word_decrypt(w.word, key), w.count) for w in s.query(Words).order_by(Words.count.desc()).all()]
