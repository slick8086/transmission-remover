#!/usr/bin/env python

import transmissionrpc
import logging
import time

# Edit config veriables below

TRANS_HOST = 'xxx.xxx.xxx.xxx'  # The host transmission is running on
TRANS_PORT = '9091' # The port the host is listening on
TRANS_USER =  'USER'    # The user id you have set
TRANS_PW = 'PASS'   # the password you have set
HASH_FILE = '/path/to/hash/file' # important file must exist, put the hashes of the file you want this program to completely ignore here
                                 # each on a separate line.(will change in the future to be in the config file)
LOG_FILE = '/path/to/log/file'   # the log file is written when something is removed
keepForDays = 2.5 # how long to keep torrents for in days (float)

# no more config variables

def loadHashesFromFile(infile):
    '''Loads hashes from a file.  These hashes will be for torrents to 
       ignore for removal. (they will not be tested for age or removed)
       takes a string for a filename as argument, return a list. 
    '''
    inFile = open(infile, 'r', 0)
    all = [ line.rstrip() for line in inFile.readlines() ]
    hashes = []
    for line in all:
        hashes.append(line)
    return hashes

def mkTime(seconds):
    '''Takes int seconds and returns a str of HH:MM:SS
    '''
    hours = seconds // 3600
    tmp = seconds - (hours * 3600)
    minutes = tmp // 60
    seconds = tmp - (minutes * 60)
    return '%02d:%02d:%02d' % (hours,minutes,seconds)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M', filename=LOG_FILE, level=logging.INFO)

tc = transmissionrpc.Client(TRANS_HOST, TRANS_PORT, TRANS_USER, TRANS_PW)

keep_hashes = loadHashesFromFile(HASH_FILE)
    
all_hashes = [torrent.hashString.encode('ascii','ignore') for torrent in tc.get_torrents() ]

del_hashes = [ x for x in all_hashes if x not in keep_hashes ]

keepForSecs = int(keepForDays * 86400) # don't change this.

for torrent in tc.get_torrents(del_hashes):
    delDate = torrent.doneDate + keepForSecs
    now = int(time.time())
    age = mkTime(now - torrent.doneDate)
    if now > delDate:
        logging.info('    remover       external        Seeded for %s, removing torrent %s', age, torrent.name)
        tc.remove_torrent(torrent.hashString)
