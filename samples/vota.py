from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)
print(wallet.getAddress())

try:
	print ('Broadcasted:', forumMan.vote ('4507febff9a801da7ed81d39110d444b2ea20b41934afa13d8bb968b50271896','Zeddiani'))
except:
	print ('Error.')