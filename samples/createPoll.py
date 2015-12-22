from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)


try:
	print ('Broadcasted:', forumMan.createPoll ('Bidda',['Zeddiani', 'Masullas', 'Ardauli'],'2015-12-19'))
except:
	print ('Error.')
	