
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

consManB = ConsensusManager.ConsensusManager ()
consManB.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
A = ForumManager.ForumManager (consMan, wallet=wallet)

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
B = ForumManager.ForumManager (consManB, wallet=wallet)

while True
	if

postid = A.createPost('Hello post', 'Post di test')
A.listPost()                                                                                   
commid = A.commentPost (postid, 'This is a comment')
A.getPostInfo(postid)
postid2 = B.createPost ('Hello post 2', 'Post di test2')
commid2 = B.commentPost (postid, 'This is a comment of B')
A.getPostInfo (postid)


pollid = A.createPoll ('Title', ['answer1', 'answer2'], '2015-12-20')
A.listPolls ()                                                                               
voteid1 = A.vote(pollid, 'answer1')
voteid2 = A.vote (pollid, 'answer2') 
B.getPollInfo (pollid)
voteid3 = B.vote (pollid, 'answer2')
A.getPollInfo (pollid)  
pollid2 = B.createPoll ('Title', ['answer1', 'answer2'], '2015-12-07')
A.listPolls ()   


A.getUserInfo ()
B.editComment (commid, 'New comment 1 message')      
print('ok')              
A.editComment (commid, 'New comment 2 message')
print('ok')
time.sleep(2) 
B.editPost (postid, 'New hello post', 'New message!') 
time.sleep(2)           
A.editPost (postid, 'New hello post A', 'New message!')

time.sleep(10)
B.listPost () 
A.deleteComment (commid)
commid3 = B.commentPost (postid, 'This is a new comment') 
time.sleep(2) 
A.deleteComment (commid3)
B.getPostInfo (postid)  
B.deletePost (postid)
time.sleep(2) 
A.deletePost (postid)
A.listPost ()
time.sleep(2) 
B.deletePoll (pollid2)
A.listPolls ()
B.getUserInfo ()
A.getUserInfo ()      

