#!/usr/bin/python3


# Author: LukeBob
#
# teamspeak AFK bot, moves afk clients to a specified channel

import sys
import time
import ts3
import ts3.definitions

minutes       = 10                       # Max idle time minutes (This is where to set your max idle time)                 
cid           = 5                        # Channel "cid" to move AFK clients to (Look up your list of channels to get id)
USER          = 'serveradmin'            # server username
PASS          = ''                       # server password
HOST          = 'localhost'              # server host
PORT          = '10011'                  # server port
SID           = 1                        # admin-sid (leave this)
MAX_IDLE_TIME = int(minutes) * 1000 * 60 # max idle time, miliseconds (leave this)


def Welcome(ts3conn): 
    while True:
        try:
            time.sleep(2)       
            clientlist = ts3conn.clientlist()
            clientlist =  [client for client in clientlist \
                           if client["client_type"] != "1"]

            for client in clientlist:            
                clid = client['clid']
                info = ts3conn.clientinfo(clid=clid)
                for ino in info:
                    try:
                        time.sleep(1)
                        if (int(ino['client_idle_time'])) > (int(MAX_IDLE_TIME)):
                            msg = ('Client: '+client['client_nickname']+' Got Moved Reason: AFK TOO LONG!')
                            ts3conn.clientmove(clid=clid, cid=cid)
                            ts3conn.gm(msg=msg)
                            #ts3conn.clientmove(clid=clid, msg=msg)               Also Poke AFK client
                            print ('Client '+client['client_nickname']+' Moved: AFK', )

                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"]:
                            continue 

                
        except ts3.query.TS3QueryError as err:
            if err.resp.error["id"]:
                continue  

def main():
    with ts3.query.TS3Connection(HOST,PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        Welcome(ts3conn)

if __name__ == '__main__':
    main()
