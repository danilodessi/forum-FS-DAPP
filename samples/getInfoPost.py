
#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)


id_post = input('Insert the id post: ')


#info = 'The post ' + id_post + ' not exists'
#v = forumMan.listPost()
#for x in v:
#	if x['id_post'] == id_post:
#		info = x['title'] + x['body']
while True:	
	print(forumMan.getPostInfo(id_post))
	time.sleep(5)