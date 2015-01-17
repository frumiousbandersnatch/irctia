#!/usr/bin/env python
'''
Access a database session
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

def get(url = 'sqlite:///:memory:', echo=True):
    if not ':' in url:
        url = 'sqlite:///' + url

    engine = create_engine(url, echo=echo)
    models.Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
