from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)

id_post = input ('Insert id post: ')
comment = input ('Insert the comment: ')


try:
	print ('Broadcasted:', forumMan.commentPost (id_post,comment))
except:
	print ('Error.')
	