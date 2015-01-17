#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Do things with weechat logs
'''

import re
import os
import sys

from datetime import datetime

import models

joinmarkers = ['▬▬▶']
partmarkers = ['◀▬▬']
actmarkers = ['◁']
infomarkers = ['--']

re_line = re.compile('(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})\t[@]?([^\t]+)[\t]?([^\t].*)?')

re_join = re.compile('([^ ]+) \(([^@]*)@(.*)\) has joined (.*)')
re_part = re.compile('([^ ]+) \(([^@]*)@(.*)\) has left ([^ ]+)[ ]?(\(.*\))?')
re_quit = re.compile('([^ ]+) \(([^@]*)@(.*)\) has quit ([^ ]+)[ ]?(\(.*\))?')
re_kick = re.compile('([^ ]+) has kicked ([^ ]+)[ ]?(\(.*\))')

#re_act =  re.compile('([^ ]+) ?(.*)?')
re_nick = re.compile('([^ ]+) is now known as (.*)')
re_mode = re.compile('Mode ([^ ]+) \[([^ ]+) (.*)\]( by ([^ ]*))?')


def parse_line (line, channel):
    'Return an object representing the parsed line'
    m = re.match(re_line, line)
    if not m:
        raise ValueError("Failed to parse line:\n%s" % line)

    g = m.groups()
    numbers = map(int, g[:6])
    stamp = datetime(*numbers)
    what = g[6]
    text = g[7]

    if what in joinmarkers:
        n,u,h,c = re.match(re_join, text).groups()
        return models.Join(channel=c, stamp=stamp, nick=n, user=u, host=h)

    if what in partmarkers:

        pm = re.match(re_part, text)
        if pm:
            n,u,h,c,_ = pm.groups()
            return models.Part(kind='part',channel=c,stamp=stamp,nick=n,user=u,host=h)

        qm = re.match(re_quit, text)
        if qm:
            n,u,h,c,_ = qm.groups()
            return models.Part(kind='quit',channel=c,stamp=stamp,nick=n,user=u,host=h)

        km = re.match(re_kick, text)
        if km:
            _, nick, _ = km.groups()
            return models.Part(kind='kick',channel=channel,stamp=stamp,nick=nick)

        return

    if what in infomarkers:
        nick_m = re.match(re_nick, text)
        if nick_m:
            old, new = nick_m.groups()
            return models.Nick(channel=channel, stamp=stamp, old=old, new=new)

        # check for ban
        mode_m = re.match(re_mode, text)
        if mode_m:
            chan, flag, mask, _, oper = mode_m.groups()
            if flag[1] != 'b': 
                return          # bail out, if add support for other Mode, rework this
            kind = flag[0]
            return models.Ban(kind=kind, channel=chan, stamp=stamp, mask=mask, oper=oper)

        return None

    return

def parse(filename, channel):
    '''
    Iterate a weechat log with message parts broken up.
    (datetime, nick, text)
    '''
    with open(filename) as fp:
        for line in fp.readlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj =  parse_line(line, channel)
            except:
                print ('Bad line: "%s"' % line)
                raise
            if not obj:
                #print ('Skipping: "%s"' % line)
                continue
            yield obj


import click
@click.command()
@click.option('-c','--channel',default="",
              help='Set channel name, default will try to guess from logfile')
@click.option('-V','--verbose', is_flag=True, default=False)
@click.argument('logfile')
@click.argument('dburl', default='sqlite://')
def backfill(channel, verbose, logfile, dburl):
    import session

    if not channel:
        if not logfile.endswith('.weechatlog'):
            click.echo("Cannot guess channel name from log file name")
            sys.exit(1)
        channel = os.path.basename(logfile).split('.')[-2]
        click.echo('Guessing channel name "%s"' % channel)
    if not channel.startswith('#'):
        channel = '#' + channel

    click.echo('Using channel: "%s"' % channel)
    
    ses = session.get(dburl, echo=verbose)
    for obj in parse(logfile, channel):
        ses.add(obj)
    ses.commit()

if '__main__' == __name__:
    for count, obj in enumerate(parse(sys.argv[1])):
        print ("%5d|%s" % (count, obj))
