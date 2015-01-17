#!/usr/bin/env python
'''
Make some queries on the database
'''

import session
from models import Join

import click
@click.command()
@click.option('-n','--nick', default=None,
              help='Set a pattern to match on the nick')
@click.option('-u','--user', default=None,
              help='Set a pattern to match on the user')
@click.option('-h','--host', default=None,
              help='Set a pattern to match on the host')
@click.option('-c','--channel',default="",
              help='Set channel name, default will try to guess from logfile')
@click.argument('dburl')
def joins(nick, user, host, channel, dburl):
    '''
    Find matching joins.
    '''
    ses = session.get(dburl)
    q = ses.query(Join)
    if nick:
        q = q.filter(Join.nick.like('%'+nick+'%'))
    if user:
        q = q.filter(Join.user.like('%'+user+'%'))
    if host:
        q = q.filter(Join.host.like('%'+host+'%'))
    q = q.order_by(Join.stamp)

    masks = set()
    for row in q:
        masks.add(row.mask)
    for m in sorted(masks):
        click.echo(m)
