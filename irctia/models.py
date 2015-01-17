#!/usr/bin/env python
'''
SQLalchemy ORM
'''

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime

class Join(Base):
    __tablename__ = 'joins'

    id = Column(Integer, primary_key=True)
    channel = Column(String, nullable = False)
    stamp = Column(DateTime, nullable = False)
    nick = Column(String, nullable = False)
    user = Column(String, nullable = False)
    host = Column(String, nullable = False)

    @property
    def mask(self):
        return '%s!%s@%s' % (self.nick, self.user, self.host)

    def __repr__(self):
        return "<Join('%s!%s@%s' joins '%s' at '%s')>" % \
            (self.nick, self.user, self.host, self.channel, self.stamp)

class Part(Base):
    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    kind = Column(String, nullable = False)
    channel = Column(String, nullable = False)
    stamp = Column(DateTime, nullable = False)
    nick = Column(String, nullable = False)
    user = Column(String)
    host = Column(String)

    @property
    def mask(self):
        return '%s!%s@%s' % (self.nick, self.user, self.host)

    def __repr__(self):
        return "<Part('%s!%s@%s' parts '%s' at '%s' by '%s')>" % \
            (self.nick, self.user, self.host, self.channel, self.stamp, self.kind)

        
class Nick(Base):
    __tablename__ = 'nicks'

    id = Column(Integer, primary_key=True)
    channel = Column(String, nullable = False)
    stamp = Column(DateTime, nullable = False)
    old = Column(String, nullable = False)
    new = Column(String, nullable = False)

    def __repr__(self):
        return "<Nick('%s' nicks '%s' on '%s' at '%s')>" % \
            (self.old, self.new, self.channel, self.stamp)


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
