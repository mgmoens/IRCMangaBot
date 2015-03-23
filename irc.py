#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import socket
import sys
import random
from google import search
 
server = "irc.irchighway.net"       # settings
channel = "#Corndog" #reddit-manga, normal channel
botnick = "tempbot"    
 
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "connecting to:"+server
irc.connect((server, 6667))
irc.send("USER " + botnick + " " + botnick + " " + botnick + " :This is a fun bot!\n")
irc.send("NICK " + botnick + "\n")                            # sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n")    # auth
irc.send("JOIN " + channel +"\n")        # join the chan
 
while 1:
    def roll():
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return str(d1 + d2)
    def usrremind(name):
        file_obj=open("list.txt", r)
        data=file_obj.read()
        index1=data.find("Usr$:"+name)
     if index1!=-1:
        index2=data.find("\n",index1) #make sure that there will always be a \n character at the end of a userlist whilst creating the crt_usrremind function
        return data[index1:index2-1]
     else: return "Person not found :( uguuuuuuuu"

     def usradd(name, toadd)
         file_obj=open("list.txt", r)
         data=file_obj.read()
         file_obj.close()
         index1=data.find("Usr$:"+name)
     if index1!=-1:
         index2=data.find("\n",index1)
         data2=data[:index2]
         data3=data[index2:]
         file_obj=open("list.txt", w)
         file_obj.write(data2+" "+toadd+data3)
         file_obj.close()
         return("added to "+name"'s list")
      else:
          file_obj=open("list.txt", a)
          file_obj.write("Usr%:"+name+" "+toadd+"\n")
          file_obj.close()
          return("created a list for"+name" and added your weebshit")

         
    text = irc.recv(2040)  # receive the text
    print text
 
    if text.find('PING') != -1:
        irc.send('PONG ' + text.split() [1] + '\r\n')
    if text.find(':!hi') != -1:
        name_raw = text.split('!')
        name = name_raw[0].replace(':', '')
        print name
        t = text.split(':!hi')
        to = t[1].strip()
        irc.send('PRIVMSG '+channel+' :Hello '+str(to)+'! \r\n')
 
    if text.find(':!roll') != -1:
        name_raw = text.split('!')
        name = name_raw[0].replace(':', '')
        irc.send('PRIVMSG '+channel+' :' + str(name) + ' rolled '+roll()+'! \r\n')


    if text.find(':!list') != -1:
        t = text.split(':!list')
        to = t[1].strip()
        too = to.replace(' ', '')
        irc.send('PRIVMSG '+channel+usrremind(to) + '\r\n')
        
 
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
