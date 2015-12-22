from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
forumMan = ForumManager.ForumManager (consMan, wallet=wallet)




#try:
print ('Broadcasted:', forumMan.deletePoll ('c04763c9c5908cb12e9f6331df197a5223c21a3ec064c270ee7ebf6e52fd4564'))
	#print ('Broadcasted:', forumMan.deleteComment('8a0054bc1f357ab8405b7833bbae3d687b896aa2451b17926e3e1b1808d67778'))
	#print(forumMan.deletePoll('7648ac4a4ab6e661e0e48daa0c5f069cb2d801f29e9b01e3b85564dcfa1ff732'))
#except:
	#print ('Error.')
	