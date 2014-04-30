#!/usr/bin/env python

import transmissionrpc
import time
import logging
from configobj import ConfigObj
from getpass import getuser
from os.path import expanduser


userdir = getuser()+"/.config/torrent-remover/"
cfgdir = expanduser('~'+userdir)
cfgFile = cfgdir + 'config.ini'

cfg = ConfigObj(cfgFile)

HASH_FILE = cfg['HASH_FILE']
LOG_FILE = cfg['LOG_FILE']
keepForDays = float(cfg['SEED_FOR'])

conn = cfg['connection']
TRANS_HOST = conn['TRANS_HOST']
TRANS_PORT = conn['TRANS_PORT']
TRANS_USER = conn['TRANS_USER']
TRANS_PASS = conn['TRANS_PASS']

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

tc = transmissionrpc.Client(TRANS_HOST, TRANS_PORT, TRANS_USER, TRANS_PASS)

keep_hashes = loadHashesFromFile(HASH_FILE)
    
all_hashes = [torrent.hashString.encode('ascii','ignore') for torrent in tc.get_torrents() ]

del_hashes = [ x for x in all_hashes if x not in keep_hashes ]

keepForSecs = int(keepForDays * 86400) # don't change this.

for torrent in tc.get_torrents(del_hashes):
	if torrent.doneDate == 0:
		continue
    delDate = torrent.doneDate + keepForSecs
    now = int(time.time())
    age = mkTime(now - torrent.doneDate)
    if now > delDate:
        logging.info('    remover       external        Seeded for %s, removing torrent %s', age, torrent.name)
        tc.remove_torrent(torrent.hashString)
