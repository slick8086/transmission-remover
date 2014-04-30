transmission-remover
====================

A python program to remove torrents from transmission that are older than a specified age.

This program uses transmission rpc api to connect to your transmission client and remove torrents that are older than a specified age.  This requires that transmission remote management is truned on in your transmission client.

transmission-remover.py reads its configuration information from ~/.config/transmission-remover/config.ini  There is an example config.ini included.

Additionally transmission-remover.py reads another file that the user specifies in the config.ini file for a list of torrent hashes to ignore. hashes.txt is included for reference. This is so that if you have some torrents that you want to seed long term transmission-remover.py will not remove them.  This program does not take into account seed ratio at all so if ratio is important to your tracker transmission-remover.py is probably not suitable for you.

transmission-remover.py is writtne in python 2.7.6 and requires external modules:
	transmissionrpc
	ConfigObj
