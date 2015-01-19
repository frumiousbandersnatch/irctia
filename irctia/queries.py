#!/usr/bin/env python
'''
Make some queries on the database
'''

import session
from models import Nick

import click

def match_join(ses, nick=None, user=None, host=None):
    q = ses.query(Nick).filter(Nick.kind == 'join')
    if nick:
        q = q.filter(Nick.new.like('%'+nick+'%'))
    if user:
        q = q.filter(Nick.user.like('%'+user+'%'))
    if host:
        q = q.filter(Nick.host.like('%'+host+'%'))
    return q.filter(Nick.kind == 'join')

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
@click.option('-V','--verbose', is_flag=True, default=False)
@click.argument('dburl')
def joins(nick, user, host, channel, formatstr, verbose, dburl):
    '''
    Find matching joins.
    '''
    ses = session.get(dburl, echo=verbose)
    q = match_join(ses, nick, user, host)

    output = set()
    for obj in q:
        string = formatstr.format(mask = obj.mask, **obj.__dict__)
        output.add(string)

    for o in sorted(output):
        click.echo(o)

def next_nick(ses, obj):
    '''
    Return the next Nick transition or None if obj is parted.
    '''
    if not obj.new:
        return

    next = ses.query(Nick)

    next = next.filter(Nick.old == obj.new)
    if not next: return

    next = next.filter(Nick.stamp >= obj.stamp)
    if not next: return

    next = next.filter(Nick.id != obj.id) 
    if not next: return         # should never run

    nick_change = next.filter(Nick.kind == 'nick')
    all_others = next.filter(Nick.kind != 'nick' and Nick.channel == obj.channel)
    next = nick_change.union(all_others)

    next = next.order_by(Nick.stamp) # ascending
    return next.first()


def iter_trail(ses, start):
    next = start
    if not next:
        return
    yield next
    
    while True:
        next = next_nick(ses, next)
        if not next:
            return
        yield next

@click.command()
@click.option('-n','--nick', default=None,
              help='Set a pattern to match on the nick')
@click.option('-u','--user', default=None,
              help='Set a pattern to match on the user')
@click.option('-h','--host', default=None,
              help='Set a pattern to match on the host')
@click.option('-t','--timestamp', default=None,
              help='Set a starting timestamp')
@click.option('-c','--channel',default="",
              help='Set channel name, default will try to guess from logfile')
@click.option('-V','--verbose', is_flag=True, default=False)
@click.argument('dburl')
def trail(nick, user, host, timestamp, channel, verbose, dburl):
    '''
    Report the trail of the a nick/user/host.
    '''
    ses = session.get(dburl, echo=verbose)
    q = match_join(ses, nick, user, host)
    if timestamp:
        q = q.filter(Nick.stamp >= timestamp)
        q = q.order_by(Nick.stamp) # ascending
    else:
        q = q.order_by(Nick.stamp.desc())
    start = q.first()
    for obj in iter_trail(ses, start):
        print ('[%s] %s %s -> %s' % (obj.kind, obj.stamp, obj.old, obj.new))

