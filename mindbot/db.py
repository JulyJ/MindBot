from datetime import datetime
from logging import getLogger
from typing import List

from sqlalchemy import (
    Column,
    create_engine,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


association_table = Table(
    'messages_tags',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('messages.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    text = Column(String)
    dt = Column(DateTime)
    sender = Column(String)
    tags = relationship('Tag', secondary=association_table, backref='messages')

    def __repr__(self):
        return '<Message id={0.id}>'.format(self)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, Sequence('tag_id_seq'), primary_key=True)
    name = Column(String, unique=True)


class DataBaseConnection:
    def __init__(self, connection_string: str):
        self._engine = create_engine(connection_string)
        Base.metadata.create_all(self._engine)
        self._session = None
        self._logger = getLogger(__name__)

    def __enter__(self):
        session_class = sessionmaker(bind=self._engine)
        self._session = session_class()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._session.close()

    def _get_or_create(self, model, **kwargs):
        instance = self._session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self._session.add(instance)
            self._session.commit()
            return instance

    def add_message(self, text: str, date: datetime, sender: str,
                    tags: List[str]):
        tags = [self._get_or_create(model=Tag, name=tag) for tag in tags]
        msg = Message(
            text=text,
            dt=date,
            sender=sender,
            tags=tags,
        )
        self._session.add(msg)
        self._session.commit()
        self._logger.debug('Message added to database. {0!r}'.format(msg))
