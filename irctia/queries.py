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
@click.option('-f','--format', 'formatstr', default="{mask}",
              help='Set the output format using Python str.format()')
@click.argument('dburl')
def joins(nick, user, host, channel, formatstr, dburl):
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

    output = set()
    for obj in q:
        string = formatstr.format(mask = obj.mask, **obj.__dict__)
        output.add(string)

    for o in sorted(output):
        click.echo(o)
