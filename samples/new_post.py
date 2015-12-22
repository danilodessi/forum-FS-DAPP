from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)

title = input ('Insert title post: ')
body = input ('Insert the message body of the post: ')


try:
	print ('Broadcasted:', forumMan.createPost (title,body))
except:
	print ('Error.')
	