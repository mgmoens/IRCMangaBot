#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import random
from google import search

server = "irc.irchighway.net"       # settings
channel = "#CornDog"
botnick = "weeabotf"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # defines the socket
print "connecting to:"+server
irc.connect((server, 6667))                                                         # connects to the server
irc.send("USER " + botnick + " " + botnick + " " + botnick + " :This is a fun bot!\n")  # user authentication
irc.send("NICK " + botnick + "\n")                            # sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n")    # auth
irc.send("JOIN " + channel +"\n")        # join the chan

while 1:
    def roll():
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return str(d1 + d2)

    text = irc.recv(2040)  # receive the text
    print text

    if text.find('PING') != -1:                          # check if 'PING' is found
        irc.send('PONG ' + text.split() [1] + '\r\n')  # returnes 'PONG' back to the server (prevents pinging out!)

    if text.find(':!hi') != -1:
        name_raw = text.split('!')
        name = name_raw[0].replace(':', '')
        print name
        t = text.split(':!hi')
        to = t[1].strip()  # this code is for getting the first word after !hi
        irc.send('PRIVMSG '+channel+' :Hello '+str(to)+'! \r\n')

    if text.find(':!roll') != -1:  # you can change !hi to whatever you want
        name_raw = text.split('!')
        name = name_raw[0].replace(':', '')
        irc.send('PRIVMSG '+channel+' :' + str(name) + ' rolled '+roll()+'! \r\n')

    if text.find(':!find') != -1:
        t = text.split(':!find')
        to = t[1].strip()
        too = to.replace(' ', '')
        irc.send('PRIVMSG '+channel+' :http://myanimelist.net/manga.php?q=' + str(to) + '\r\n')

    if text.find(':!try') != -1:
        t = text.split(':!try')
        urls = []
        to = t[1].strip()
        too = to.replace(' ', '')
        que = search((to + ' mangaupdates'), tld='es', lang='es', stop=1)
        for i in que:
            if 'mangaupdates.com' in i:
                urls.append(i)
        try:
            if urls[0] == 'https://www.mangaupdates.com/series.html?id=26776':
                try:
                    print 'working'
                    print urls[0]
                    irc.send('PRIVMSG '+channel+' :' + str(urls[0]) + " ( ͡° ͜ʖ ͡°)" + '\r\n')
                except:
                    pass
        except:
            pass
        else:
            try:
                irc.send('PRIVMSG '+channel+' :' + str(urls[0]) + '\r\n')
            except:
                irc.send('PRIVMSG '+channel+' :Error.' + '\r\n')