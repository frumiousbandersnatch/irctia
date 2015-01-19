#!/usr/bin/env python
'''
SQLalchemy ORM
'''

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint

class Nick(Base):

    __tablename__ = 'nicks'

    id = Column(Integer, primary_key=True)
    # join, part, quit, kick, nick
    kind = Column(String, nullable = False)
    channel = Column(String, nullable = False)
    stamp = Column(DateTime, nullable = False)
    new = Column(String)
    old = Column(String)
    user = Column(String)
    host = Column(String)

    CheckConstraint("new or old", "need_a_nick")

    @property
    def nick(self):
        return self.new or self.old

    @property
    def mask(self):
        return '%s!%s@%s' % (self.nick, self.user, self.host)

class Ban(Base):
    __tablename__ = 'bans'

    id = Column(Integer, primary_key=True)
    kind = Column(String, nullable = False)
    channel = Column(String, nullable = False)
    stamp = Column(DateTime, nullable = False)
    mask = Column(String, nullable = False)
    oper = Column(String, nullable = False)

    def __repr__(self):
        return "<Ban('%s' %sb'ed from '%s' by '%s' at '%s')>" % \
            (self.mask, self.kind, self.channel, self.oper, self.stamp)
