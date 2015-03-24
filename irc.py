#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import random
from google import search
#Gets variables from config.py
from config import *
#for exit
import sys

#function for init connection
def ircConnect():
    #defines the socket
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print "connecting to:"+server

    #connects to the server
    irc.connect((server, 6667))

    #user authentication                                                         
    irc.send("USER " + botnick + " " + botnick + " " + botnick + " :This is a fun bot!\n")  

    #sets nick
    irc.send("NICK " + botnick + "\n")

    #auth                            
    irc.send("PRIVMSG nickserv :iNOOPE\r\n")  

    #join the chan  
    irc.send("JOIN " + channel +"\n")    
    return irc

def usrremind(name):
    file_obj = open("list.txt", 'r')
    data = file_obj.read()
    file_obj.close()
    index1 = data.find('Usr%:'+name)
    if index1 != -1:
        index2 = data.find("\n", index1)
        return data[index1:index2]
    return 'Person not found :( uguuuuuuuu'

def usradd(name, toadd):
    file_obj = open("list.txt", 'r')
    data = file_obj.read()
    file_obj.close()
    index1 = data.find("Usr%:"+name)
    if index1 != -1:
        index2 = data.find("\n", index1)
        data2 = data[:index2]
        data3 = data[index2:]
        file_obj = open("list.txt", 'w')
        file_obj.write(data2+"" + ', ' +toadd+data3)
        file_obj.close()
        return 'added to ' + name + '\'s list'
    else:
        file_obj = open("list.txt", 'a')
        file_obj.write("Usr%:"+name+" "+toadd + "\n")
        file_obj.close()
        return 'created a list for ' + name + ' and added your weebshit'

#utility functions
def get_name(text):
    #doesnt work
    #t = text.split('!')
    #t0 = t[0].split(':')[1]
    return text[text.find(':')+1:text.find('!')]

def trigger(text, trigger):
    #get 4th word in text
    command = text.split()[3]
    if(command.find(':!'+trigger) != -1):
        return True
    else:
        return False

def sendMessage(irc, channel, message):
    irc.send('PRIVMSG '+channel+' :'+message+'\r\n')
    return

def sendPM(irc, name, message):
    irc.send('PRIVMSG '+name+' : '+message + '\r\n')
    return


#########################
### START OF COMMANDS ###
#########################

#Command for !hi
def hiCMD(irc, text):
    mess = 'Hello !'
    sendMessage(irc, channel, mess)
    return

#Command for !roll
def rollCMD(irc, text):
    name_raw = text.split('!')
    name = name_raw[0].replace(':', '')
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    irc.send('PRIVMSG '+channel+' :' + str(name) + ' rolled '+str(d1 + d2)+'! \r\n')
    return

#Command for !find
def findCMD(irc, text):
    t = text.split(':!find')
    to = t[1].strip()
    too = to.replace(' ', '')
    irc.send('PRIVMSG '+channel+' :http://myanimelist.net/manga.php?q=' + str(to) + '\r\n')
    return

#Command for !try
def tryCMD(irc, text):
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
                print 'urls[0]'
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
    return

#Command for !name
def nameCMD(irc, text):
    name = get_name(text)
    irc.send('PRIVMSG '+channel+' :'+name+'\r\n')
    return

#Command for !list
def listCMD(irc, text):
    t = text.split(':!list')
    to = t[1].strip()
    try:
        fin = usrremind(get_name(text)).split('Usr%:')
        fin2 = fin[1].strip()
        irc.send('NOTICE '+get_name(text)+' :'+fin2 + '\r\n')
    except:
        pass
    return

#Command for !add
def addCMD(irc, text):
    t = text.split(':!add')
    to = t[1].strip()
    irc.send('NOTICE '+get_name(text)+' :' + ' ' + usradd(get_name(text), to) + '\r\n')
    return
#########################
###  END OF COMMANDS  ###
#########################


#Main Program
irc = ircConnect()
while 1:
    #receive the text
    text = irc.recv(2040)  
    print text

    if text.find('PING') != -1:                        # check if 'PING' is found
        irc.send('PONG ' + text.split() [1] + '\r\n')  # returnes 'PONG' back to the server (prevents pinging out!)

    #TODO:Check a list of admin nicks
    if trigger(text, 'quit') and text.find('Kamo') != -1: 
        sys.exit()

    if trigger(text, 'hi'):
        hiCMD(irc, text)

    if trigger(text, 'roll'):
        rollCMD(irc, text)

    if trigger(text, 'find'):
        findCMD(irc, text)

    if trigger(text, 'try'):
        tryCMD(irc, text)

    if trigger(text, 'name'):
        nameCMD(irc, text)
        
    if trigger(text, 'list'):
        listCMD(irc, text)

    if trigger(text, 'add'):
        addCMD(irc, text)

    if trigger(text, 'help'):
        name = get_name(text)
        t1 = ' This is an open-source bot: you can look at the source at https://github.com/phaseout/IRCMangaBot.git'
        t2 = ' !roll rolls a six sided dice, for you'
        t3 = ' !add (title) adds a title to your personal plain text backlog! !list (name) returns that persons list'
        t4 = ' !try makes me search baka, you b-baka!'
        sendPM(irc, name, t1)
        sendPM(irc, name, t2)
        sendPM(irc, name, t3)
        sendPM(irc, name, t4)

